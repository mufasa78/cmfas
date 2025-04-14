from flask import render_template, request, jsonify, redirect, url_for, flash, session, g
from datetime import datetime, timezone
from functools import wraps
from app import app, db
from models import (
    MedicinalMaterial, Prescription, EfficacyCategory,
    FormulaOptimization, DataImport, User, UserActivity
)
from translations import get_text
from language import get_language, set_language
from data_processing import (
    get_province_statistics, get_material_usage_frequency,
    get_property_distribution, get_flavor_distribution, get_meridian_distribution,
    get_top_prescriptions_by_efficacy, get_top_materials_by_efficacy,
    process_material_upload, process_prescription_upload, search_prescriptions
)
from ml_models import FormulaOptimizer, MaterialClusterer
from knowledge_graph import (
    build_knowledge_graph, get_material_subgraph,
    get_prescription_subgraph
)
import logging

logger = logging.getLogger(__name__)

# User loader from session
@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            flash(get_text('login_required', get_language()), 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# Admin required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None or not g.user.is_admin:
            flash(get_text('admin_required', get_language()), 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# Log user activity
def log_user_activity(user_id, action, details=None):
    try:
        activity = UserActivity(
            user_id=user_id,
            action=action,
            details=details,
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string if request.user_agent else None
        )
        db.session.add(activity)
        db.session.commit()
    except Exception as e:
        app.logger.error(f"Error logging user activity: {e}")
        db.session.rollback()

# Authentication routes
@app.route("/login", methods=["GET", "POST"])
def login():
    if g.user:
        return redirect(url_for('index'))

    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        remember = 'remember' in request.form

        user = User.query.filter_by(username=username).first()

        if user is None or not user.check_password(password):
            error = get_text('invalid_credentials', get_language())
        elif not user.is_active:
            error = get_text('account_inactive', get_language())
        else:
            # Login successful
            session.clear()
            session['user_id'] = user.id

            # Update last login time
            user.last_login = datetime.now(timezone.utc)
            db.session.commit()

            # Log activity
            log_user_activity(user.id, 'login')

            # Set session permanence based on remember checkbox
            session.permanent = remember

            # Redirect to next page or index
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('index')

            flash(get_text('login_success', get_language()), 'success')
            return redirect(next_page)

    return render_template(
        "login.html",
        title=get_text('login', get_language()),
        error=error,
        lang=get_language(),
        t=lambda key, *args: get_text(key, get_language(), *args)
    )

@app.route("/register", methods=["GET", "POST"])
def register():
    if g.user:
        return redirect(url_for('index'))

    error = None
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        agree_terms = 'agree_terms' in request.form

        # Validate input
        if not username or not email or not password or not confirm_password:
            error = get_text('all_fields_required', get_language())
        elif not agree_terms:
            error = get_text('must_agree_terms', get_language())
        elif password != confirm_password:
            error = get_text('passwords_not_match', get_language())
        elif len(password) < 8:
            error = get_text('password_too_short', get_language())
        elif User.query.filter_by(username=username).first():
            error = get_text('username_exists', get_language())
        elif User.query.filter_by(email=email).first():
            error = get_text('email_exists', get_language())
        else:
            # Create new user
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()

            # Log activity
            log_user_activity(user.id, 'register')

            # Auto-login after registration
            session.clear()
            session['user_id'] = user.id

            flash(get_text('register_success', get_language()), 'success')
            return redirect(url_for('index'))

    return render_template(
        "register.html",
        title=get_text('register', get_language()),
        error=error,
        lang=get_language(),
        t=lambda key, *args: get_text(key, get_language(), *args)
    )

@app.route("/logout")
def logout():
    if g.user:
        user_id = session.get('user_id')
        log_user_activity(user_id, 'logout')

    session.clear()
    flash(get_text('logout_success', get_language()), 'success')
    return redirect(url_for('index'))

@app.route("/profile")
@login_required
def profile():
    # Get user activity logs
    activities = UserActivity.query.filter_by(user_id=g.user.id).order_by(UserActivity.timestamp.desc()).limit(10).all()

    return render_template(
        "profile.html",
        title=get_text('profile', get_language()),
        user=g.user,
        activities=activities,
        lang=get_language(),
        t=lambda key, *args: get_text(key, get_language(), *args)
    )

@app.route("/update-preferences", methods=["POST"])
@login_required
def update_preferences():
    language = request.form.get("language")
    theme = request.form.get("theme")

    if language in ['en', 'zh']:
        # Update user preferences in database
        g.user.preferences['language'] = language
        g.user.preferences['theme'] = theme
        db.session.commit()

        # Update session language
        set_language(language)

        # Log activity
        log_user_activity(g.user.id, 'update_preferences', f"language: {language}, theme: {theme}")

        flash(get_text('preferences_updated', get_language()), 'success')

    return redirect(url_for('profile'))

@app.route("/change-password", methods=["POST"])
@login_required
def change_password():
    current_password = request.form.get("current_password")
    new_password = request.form.get("new_password")
    confirm_new_password = request.form.get("confirm_new_password")

    if not current_password or not new_password or not confirm_new_password:
        flash(get_text('all_fields_required', get_language()), 'danger')
    elif not g.user.check_password(current_password):
        flash(get_text('current_password_incorrect', get_language()), 'danger')
    elif new_password != confirm_new_password:
        flash(get_text('passwords_not_match', get_language()), 'danger')
    elif len(new_password) < 8:
        flash(get_text('password_too_short', get_language()), 'danger')
    else:
        g.user.set_password(new_password)
        db.session.commit()

        # Log activity
        log_user_activity(g.user.id, 'change_password')

        flash(get_text('password_changed', get_language()), 'success')

    return redirect(url_for('profile'))

@app.route("/request-password-reset", methods=["GET", "POST"])
def request_password_reset():
    if g.user:
        return redirect(url_for('index'))

    error = None
    success = None

    if request.method == "POST":
        email = request.form.get("email")
        user = User.query.filter_by(email=email).first()

        if not email:
            error = get_text('email_required', get_language())
        elif not user:
            # Don't reveal that the user doesn't exist
            success = get_text('reset_link_sent', get_language())
        else:
            # In a real application, send a password reset email here
            # For this demo, we'll just show a success message
            success = get_text('reset_link_sent', get_language())

            # Log activity
            log_user_activity(user.id, 'request_password_reset')

    return render_template(
        "request_password_reset.html",
        title=get_text('reset_password', get_language()),
        error=error,
        success=success,
        lang=get_language(),
        t=lambda key, *args: get_text(key, get_language(), *args)
    )

# Language route (for switching language)
@app.route("/language/<lang>")
def change_language(lang):
    if lang in ['en', 'zh']:
        set_language(lang)

        # Update user preferences if logged in
        if g.user:
            g.user.preferences['language'] = lang
            db.session.commit()

    return redirect(request.referrer or url_for('index'))

# Test authentication route
@app.route("/test-auth")
def test_auth():
    return render_template(
        "test_auth.html",
        title="Authentication Test",
        lang=get_language(),
        t=lambda key, *args: get_text(key, get_language(), *args)
    )

# Home route
@app.route("/")
def index():
    # Get some basic statistics for dashboard
    total_materials = MedicinalMaterial.query.count()
    total_prescriptions = Prescription.query.count()
    total_efficacies = EfficacyCategory.query.count()

    # Get recent prescriptions
    recent_prescriptions = Prescription.query.order_by(Prescription.created_at.desc()).limit(5).all()

    # Get top used materials
    top_materials = db.session.query(MedicinalMaterial).order_by(
        MedicinalMaterial.usage_frequency.desc()
    ).limit(5).all()

    # Get current language
    lang = get_language()

    return render_template(
        "index_translated.html",
        title=get_text('site_title', lang),
        total_materials=total_materials,
        total_prescriptions=total_prescriptions,
        total_efficacies=total_efficacies,
        recent_prescriptions=recent_prescriptions,
        top_materials=top_materials,
        lang=lang,
        t=lambda key, *args: get_text(key, lang, *args)
    )

# Province statistics route
@app.route("/province-stats")
def province_stats():
    stats = get_province_statistics()
    lang = get_language()
    return render_template(
        "province_stats.html",
        title=get_text('province_stats', lang),
        stats=stats,
        lang=lang,
        t=lambda key, *args: get_text(key, lang, *args)
    )

# Material usage frequency route
@app.route("/material-stats")
def material_stats():
    lang = get_language()
    return render_template(
        "material_stats.html",
        title=get_text('material_usage', lang),
        lang=lang,
        t=lambda key, *args: get_text(key, lang, *args)
    )

# API endpoint for material usage data
@app.route("/api/material-usage")
def api_material_usage():
    data = get_material_usage_frequency()
    return jsonify(data)

# Property, flavor, and meridian distribution route
@app.route("/property-distribution")
def property_distribution():
    properties = get_property_distribution()
    flavors = get_flavor_distribution()
    meridians = get_meridian_distribution()
    lang = get_language()

    return render_template(
        "property_distribution.html",
        title=get_text('property_distribution', lang),
        properties=properties,
        flavors=flavors,
        meridians=meridians,
        lang=lang,
        t=lambda key, *args: get_text(key, lang, *args)
    )

# Top prescriptions by efficacy route
@app.route("/top-prescriptions")
def top_prescriptions():
    # Get all efficacy categories
    categories = EfficacyCategory.query.all()

    # Use the first category by default or get from query parameter
    selected_category = request.args.get('category')
    if not selected_category and categories:
        selected_category = categories[0].name

    # Get top prescriptions and materials for the selected category
    prescriptions = get_top_prescriptions_by_efficacy(selected_category)
    materials = get_top_materials_by_efficacy(selected_category)

    lang = get_language()
    return render_template(
        "top_prescriptions.html",
        title=f"{get_text('top_prescriptions', lang)} - {selected_category}",
        categories=categories,
        selected_category=selected_category,
        prescriptions=prescriptions,
        materials=materials,
        lang=lang,
        t=lambda key, *args: get_text(key, lang, *args)
    )

# Prescription entry route
@app.route("/prescription-entry", methods=["GET", "POST"])
def prescription_entry():
    if request.method == "POST":
        try:
            # Get form data
            name = request.form.get("name")
            description = request.form.get("description")
            efficacy = request.form.get("efficacy")

            # Check if prescription already exists
            existing = Prescription.query.filter_by(name=name).first()
            if existing:
                flash(f"Prescription '{name}' already exists", "warning")
                return redirect(url_for("prescription_entry"))

            # Create new prescription
            prescription = Prescription(
                name=name,
                description=description,
                efficacy=efficacy,
                evolution_history={}
            )

            # Add materials
            material_names = request.form.getlist("materials")
            for material_name in material_names:
                material = MedicinalMaterial.query.filter_by(name=material_name).first()
                if material:
                    prescription.materials.append(material)
                    # Increment usage frequency
                    material.usage_frequency += 1

            # Add efficacy categories
            efficacy_cats = request.form.get("efficacy_categories", "").split(",")
            for cat_name in efficacy_cats:
                cat_name = cat_name.strip()
                if cat_name:
                    category = EfficacyCategory.query.filter_by(name=cat_name).first()
                    if not category:
                        category = EfficacyCategory(name=cat_name)
                        db.session.add(category)
                    prescription.efficacy_categories.append(category)

            db.session.add(prescription)
            db.session.commit()

            flash(f"Prescription '{name}' added successfully", "success")
            return redirect(url_for("prescription_entry"))

        except Exception as e:
            db.session.rollback()
            flash(f"Error adding prescription: {str(e)}", "danger")

    # Get all materials for the form
    materials = MedicinalMaterial.query.order_by(MedicinalMaterial.name).all()
    categories = EfficacyCategory.query.order_by(EfficacyCategory.name).all()

    lang = get_language()
    return render_template(
        "prescription_entry.html",
        title=get_text('add_prescription', lang),
        materials=materials,
        categories=categories,
        lang=lang,
        t=lambda key, *args: get_text(key, lang, *args)
    )

# Prescription search route
@app.route("/prescription-search")
def prescription_search():
    query_params = {
        'name': request.args.get('name', ''),
        'efficacy': request.args.get('efficacy', ''),
        'material': request.args.get('material', ''),
        'category': request.args.get('category', '')
    }

    # Only search if at least one parameter is provided
    results = []
    if any(query_params.values()):
        results = search_prescriptions(query_params)

    # Get all materials and categories for the search form
    materials = MedicinalMaterial.query.order_by(MedicinalMaterial.name).all()
    categories = EfficacyCategory.query.order_by(EfficacyCategory.name).all()

    lang = get_language()
    return render_template(
        "prescription_search.html",
        title=get_text('search_prescriptions', lang),
        results=results,
        query=query_params,
        materials=materials,
        categories=categories,
        lang=lang,
        t=lambda key, *args: get_text(key, lang, *args)
    )

# Data import route
@app.route("/data-import", methods=["GET", "POST"])
def data_import():
    if request.method == "POST":
        import_type = request.form.get("import_type")
        file = request.files.get("file")

        if not file:
            flash("No file selected", "danger")
            return redirect(url_for("data_import"))

        try:
            file_data = file.read()
            filename = file.filename

            if import_type == "materials":
                success_count, error_count, error_messages = process_material_upload(file_data)
            elif import_type == "prescriptions":
                success_count, error_count, error_messages = process_prescription_upload(file_data)
            else:
                flash("Invalid import type", "danger")
                return redirect(url_for("data_import"))

            # Log the import
            status = "success" if error_count == 0 else "partial" if success_count > 0 else "error"
            error_message = "\n".join(error_messages) if error_messages else None

            import_log = DataImport(
                filename=filename,
                import_type=import_type,
                rows_imported=success_count,
                status=status,
                error_message=error_message
            )
            db.session.add(import_log)
            db.session.commit()

            # Flash message
            if error_count == 0:
                flash(f"Successfully imported {success_count} {import_type}", "success")
            else:
                flash(f"Imported {success_count} {import_type} with {error_count} errors", "warning")
                for error in error_messages:
                    flash(error, "danger")

            return redirect(url_for("data_import"))

        except Exception as e:
            db.session.rollback()
            flash(f"Error processing file: {str(e)}", "danger")

    # Get import logs
    import_logs = DataImport.query.order_by(DataImport.import_date.desc()).limit(10).all()

    lang = get_language()
    return render_template(
        "data_import.html",
        title=get_text('import_data', lang),
        import_logs=import_logs,
        lang=lang,
        t=lambda key, *args: get_text(key, lang, *args)
    )

# Formula optimization route
@app.route("/formula-optimization", methods=["GET", "POST"])
def formula_optimization():
    if request.method == "POST":
        symptoms = request.form.get("symptoms")

        # Get selected base materials
        base_materials = request.form.getlist("base_materials")

        if not symptoms:
            flash("Please enter symptoms", "warning")
            return redirect(url_for("formula_optimization"))

        try:
            # Initialize optimizer
            optimizer = FormulaOptimizer()

            # Optimize formula
            result = optimizer.optimize_formula(symptoms, base_materials)

            if result["success"]:
                # Store in session for display
                session['optimization_result'] = result
                flash("Formula optimization successful", "success")
            else:
                flash(f"Formula optimization failed: {result.get('message', 'Unknown error')}", "danger")

            return redirect(url_for("formula_optimization"))

        except Exception as e:
            flash(f"Error optimizing formula: {str(e)}", "danger")

    # Get all materials for the form
    materials = MedicinalMaterial.query.order_by(MedicinalMaterial.name).all()

    # Get optimization result from session if available
    optimization_result = session.pop('optimization_result', None)

    # Get recent optimizations
    recent_optimizations = FormulaOptimization.query.order_by(
        FormulaOptimization.created_at.desc()
    ).limit(5).all()

    lang = get_language()
    return render_template(
        "formula_optimization.html",
        title=get_text('formula_optimization', lang),
        materials=materials,
        optimization_result=optimization_result,
        recent_optimizations=recent_optimizations,
        lang=lang,
        t=lambda key, *args: get_text(key, lang, *args)
    )

# Knowledge graph route
@app.route("/knowledge-graph")
def knowledge_graph():
    lang = get_language()
    return render_template(
        "knowledge_graph.html",
        title=get_text('knowledge_graph', lang),
        lang=lang,
        t=lambda key, *args: get_text(key, lang, *args)
    )

# API endpoint for knowledge graph data
@app.route("/api/knowledge-graph")
def api_knowledge_graph():
    material_id = request.args.get('material_id')
    prescription_id = request.args.get('prescription_id')

    if material_id:
        # Get subgraph centered on material
        graph_data = get_material_subgraph(int(material_id))
    elif prescription_id:
        # Get subgraph centered on prescription
        graph_data = get_prescription_subgraph(int(prescription_id))
    else:
        # Get full graph (with limit to avoid browser hanging)
        full_graph = build_knowledge_graph()

        # Limit to a reasonable number of nodes
        max_nodes = 100
        if len(full_graph['nodes']) > max_nodes:
            # Filter to keep only the most used materials and their connected prescriptions
            material_nodes = [node for node in full_graph['nodes'] if node['type'] == 'material']
            material_nodes.sort(key=lambda x: x.get('usage_frequency', 0), reverse=True)

            # Keep top materials
            top_materials = material_nodes[:max_nodes // 2]
            top_material_ids = [node['id'] for node in top_materials]

            # Filter links to keep only those connected to top materials
            filtered_links = [link for link in full_graph['links']
                            if link['source'] in top_material_ids or link['target'] in top_material_ids]

            # Get connected prescription IDs
            connected_prescription_ids = set()
            for link in filtered_links:
                if link['source'].startswith('p_'):
                    connected_prescription_ids.add(link['source'])
                if link['target'].startswith('p_'):
                    connected_prescription_ids.add(link['target'])

            # Filter nodes to keep only top materials and connected prescriptions
            filtered_nodes = top_materials + [
                node for node in full_graph['nodes']
                if node['type'] == 'prescription' and node['id'] in connected_prescription_ids
            ]

            graph_data = {
                'nodes': filtered_nodes[:max_nodes],
                'links': filtered_links
            }
        else:
            graph_data = full_graph

    return jsonify(graph_data)

# API endpoint for material clustering
@app.route("/api/material-clusters")
def api_material_clusters():
    clusterer = MaterialClusterer()
    cluster_data = clusterer.get_cluster_data()
    return jsonify(cluster_data)

# API endpoint to get prescription details
@app.route("/api/prescription/<int:prescription_id>")
def api_prescription_details(prescription_id):
    prescription = Prescription.query.get_or_404(prescription_id)

    materials = [
        {
            'id': material.id,
            'name': material.name,
            'property': material.property,
            'flavor': material.flavor,
            'meridian': material.meridian
        }
        for material in prescription.materials
    ]

    efficacy_categories = [
        {
            'id': category.id,
            'name': category.name
        }
        for category in prescription.efficacy_categories
    ]

    return jsonify({
        'id': prescription.id,
        'name': prescription.name,
        'description': prescription.description,
        'efficacy': prescription.efficacy,
        'materials': materials,
        'efficacy_categories': efficacy_categories,
        'created_at': prescription.created_at.isoformat() if prescription.created_at else None
    })

# API endpoint to get material details
@app.route("/api/material/<int:material_id>")
def api_material_details(material_id):
    material = MedicinalMaterial.query.get_or_404(material_id)

    prescription_count = len(material.prescriptions)

    return jsonify({
        'id': material.id,
        'name': material.name,
        'pinyin': material.pinyin,
        'english_name': material.english_name,
        'province_origin': material.province_origin,
        'property': material.property,
        'flavor': material.flavor,
        'meridian': material.meridian,
        'description': material.description,
        'usage_frequency': material.usage_frequency,
        'prescription_count': prescription_count
    })
