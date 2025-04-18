"""
Translations for Chinese and English languages
"""

translations = {
    'en': {
        # Authentication
        'login': 'Login',
        'register': 'Register',
        'logout': 'Logout',
        'profile': 'Profile',
        'username': 'Username',
        'email': 'Email',
        'password': 'Password',
        'confirm_password': 'Confirm Password',
        'current_password': 'Current Password',
        'new_password': 'New Password',
        'confirm_new_password': 'Confirm New Password',
        'remember_me': 'Remember me',
        'forgot_password': 'Forgot your password?',
        'reset_password': 'Reset Password',
        'change_password': 'Change Password',
        'update_password': 'Update Password',
        'send_reset_link': 'Send Reset Link',
        'create_new_password': 'Create a new password for your account.',
        'back_to_login': 'Back to Login',
        'login_success': 'Login successful.',
        'login_failed': 'Login failed. Please check your username and password.',
        'logout_success': 'You have been logged out.',
        'register_success': 'Registration successful.',
        'register_failed': 'Registration failed. Please try again.',
        'passwords_not_match': 'Passwords do not match.',
        'email_invalid': 'Invalid email address.',
        'username_exists': 'Username already exists.',
        'email_exists': 'Email already exists.',
        'welcome_user': 'Welcome, {}',
        'account_inactive': 'Your account is inactive. Please contact support.',
        'login_required': 'You need to be logged in to access this page.',
        'admin_required': 'You need to be an admin to access this page.',
        'email_verification': 'Email Verification',
        'invalid_credentials': 'Invalid username or password.',
        'all_fields_required': 'All fields are required.',
        'must_agree_terms': 'You must agree to the terms and conditions.',
        'password_too_short': 'Password must be at least 8 characters long.',
        'current_password_incorrect': 'Current password is incorrect.',
        'password_changed': 'Your password has been changed successfully.',
        'preferences_updated': 'Your preferences have been updated.',
        'reset_link_sent': 'A password reset link has been sent to your email.',
        'reset_password_instructions': 'Enter your email address and we will send you a link to reset your password.',
        'no_account': 'Don\'t have an account?',
        'register_now': 'Register now',
        'already_have_account': 'Already have an account?',
        'login_now': 'Login now',
        'agree_terms': 'I agree to the terms and conditions',
        'username_requirements': 'Username must be 3-20 characters long and contain only letters, numbers, and underscores.',
        'password_requirements': 'Password must be at least 8 characters long.',
        'profile_info': 'Profile Information',
        'account_settings': 'Account Settings',
        'preferences': 'Preferences',
        'security': 'Security',
        'activity': 'Activity',
        'language': 'Language',
        'theme': 'Theme',
        'light': 'Light',
        'dark': 'Dark',
        'save_preferences': 'Save Preferences',
        'action': 'Action',
        'timestamp': 'Timestamp',
        'details': 'Details',
        'no_activity_records': 'No activity records found.',
        'active_user': 'Active User',
        'admin': 'Administrator',
        'member_since': 'Member since',
        'user_id': 'User ID',
        'verify_email': 'Verify Email',
        'verification_success': 'Email Verified Successfully!',
        'verification_failed': 'Verification Failed',
        'verification_success_message': 'Your email has been verified successfully. You can now access all features of the application.',
        'verification_failed_message': 'The verification link is invalid or has expired.',
        'already_verified': 'Your email is already verified.',
        'verification_sent': 'Verification email sent. Please check your inbox.',
        'email_required': 'Please enter your email address.',
        'reset_password_sent': 'If your email address exists in our database, you will receive a password recovery link at your email address in a few minutes.',
        'reset_password_instructions': 'Enter your email address and we will send you a link to reset your password.',
        'invalid_token': 'The password reset link is invalid or has expired.',
        'password_required': 'Please enter a new password.',
        'password_reset_success': 'Your password has been reset. You can now log in with your new password.',
        'all_fields_required': 'All fields are required.',
        'current_password_incorrect': 'Current password is incorrect.',
        'password_updated': 'Your password has been updated.',
        'preferences_updated': 'Your preferences have been updated.',
        'no_account': 'Don\'t have an account?',
        'already_have_account': 'Already have an account?',
        'account_info': 'Account Information',
        'preferences': 'Preferences',
        'security': 'Security',
        'activity_log': 'Activity Log',
        'no_activity_logs': 'No activity logs found.',
        'member_since': 'Member since',
        'last_login': 'Last Login',
        'email_verified': 'Email Verified',
        'email_not_verified': 'Email Not Verified',
        'default_language': 'Default Language',
        'theme': 'Theme',
        'light_theme': 'Light',
        'dark_theme': 'Dark',
        'enable_notifications': 'Enable Notifications',
        'save_changes': 'Save Changes',
        'action': 'Action',
        'details': 'Details',
        'ip_address': 'IP Address',
        'not_available': 'N/A',
        # Import data page
        'import_data_description': 'Use this form to import data into the system. You can upload CSV files containing information about medicinal materials or prescriptions. Make sure your file follows the required format.',
        'import_type': 'Import Type',
        'select_import_type': 'Select import type',
        'csv_file': 'CSV File',
        'upload_csv_instruction': 'Upload a CSV file with the data to import.',
        'reset': 'Reset',
        'upload_and_process': 'Upload and Process',
        'recent_import_logs': 'Recent Import Logs',
        'date': 'Date',
        'filename': 'Filename',
        'type': 'Type',
        'rows_imported': 'Rows Imported',
        'status': 'Status',
        'success': 'Success',
        'partial': 'Partial',
        'error': 'Error',
        'import_errors': 'Import Errors',
        'close': 'Close',
        'no_import_logs': 'No import logs found. Start by importing some data.',
        'medicinal_materials_csv_format': 'Medicinal Materials CSV Format',
        'materials_csv_description': 'Your CSV file for medicinal materials should contain the following columns:',
        'column': 'Column',
        'description': 'Description',
        'required': 'Required',
        'material_name_description': 'Name of the medicinal material',
        'pinyin_description': 'Pinyin transliteration',
        'english_name_description': 'English name of the material',
        'province_origin_description': 'Province where the material originates',
        'property_description': 'Five properties (cold, hot, warm, cool, neutral)',
        'flavor_description': 'Five flavors (sour, bitter, sweet, spicy, salty)',
        'meridian_description': 'Meridian tropism (which organ/meridian it affects)',
        'material_description_field': 'Description of the material',
        'yes': 'Yes',
        'no': 'No',
        'example': 'Example',
        'prescriptions_csv_format': 'Prescriptions CSV Format',
        'prescriptions_csv_description': 'Your CSV file for prescriptions should contain the following columns:',
        'prescription_name_description': 'Name of the prescription',
        'prescription_description_field': 'Description of the prescription',
        'efficacy_description': 'What the prescription treats',
        'materials_format_description': 'List of materials in format: "name1:amount1,name2:amount2"',
        'efficacy_categories_description': 'Comma-separated list of efficacy categories',
        'note': 'Note',
        'materials_prerequisite_warning': 'Materials must already exist in the database before importing prescriptions that reference them.',
        # Common elements
        'site_title': 'Chinese Medicine Prescription Analysis',
        'dashboard': 'Dashboard',
        'analytics': 'Analytics',
        'prescriptions': 'Prescriptions',
        'formula_optimization': 'Formula Optimization',
        'knowledge_graph': 'Knowledge Graph',
        'import_data': 'Import Data',
        'welcome': 'Welcome to the Chinese Medicine Prescription Analysis System',
        'welcome_description': 'This platform provides tools for analyzing traditional Chinese medicine prescriptions, visualizing medicinal material usage patterns, and optimizing formulations based on machine learning.',

        # Dashboard statistics
        'medicinal_materials': 'Medicinal Materials',
        'prescription_formulas': 'Prescription Formulas',
        'efficacy_categories': 'Efficacy Categories',
        'recent_prescriptions': 'Recent Prescriptions',
        'top_materials': 'Top Used Materials',
        'view_all': 'View All',
        'quick_analysis': 'Quick Analysis',
        'no_prescriptions': 'No prescriptions found. Add a prescription to get started.',
        'no_materials': 'No medicinal materials found. Import data to get started.',

        # Province stats page
        'province_stats': 'Province Statistics',
        'materials_by_province': 'Medicinal Materials by Province',
        'province_stats_description': 'This visualization shows the distribution of medicinal materials produced in each province across China. Understanding regional production patterns helps in analyzing the geographical characteristics of Chinese medicine resources.',

        # Material usage page
        'material_usage': 'Material Usage Statistics',
        'usage_frequency': 'Usage Frequency',
        'usage_distribution': 'Usage Distribution',
        'usage_frequency_description': 'This visualization shows the frequency of use of each medicinal material across all prescriptions in the database. Materials that appear more frequently are essential components in traditional Chinese medicine.',
        'material_usage_distribution': 'Material Usage Distribution',
        'material_usage_insights': 'Material Usage Insights',
        'key_insights': 'Key Insights:',
        'insight_1': 'The top used materials often indicate core components in traditional formulations',
        'insight_2': 'Materials with high usage frequency typically have broad therapeutic applications',
        'insight_3': 'Understanding usage patterns helps in optimizing new formulations',
        'insight_4': 'Regional variations may affect material availability and prescription customization',
        'tip': 'Tip:',
        'usage_tip': 'Compare material usage with efficacy categories to identify specialized materials for specific conditions.',
        'view_top_prescriptions': 'View Top Prescriptions',
        'material_clustering': 'Material Clustering',
        'clustering_description': 'This visualization clusters medicinal materials based on their properties, flavors, and usage patterns. Similar materials are grouped together, revealing natural categories within Chinese medicine pharmacology.',

        # Property distribution page
        'property_distribution': 'Distribution of Properties, Flavors, and Meridians',
        'tcm_attributes_intro': 'In traditional Chinese medicine, medicinal materials are classified by three key attributes:',
        'five_properties': 'Five Properties (五性):',
        'five_properties_desc': 'Cold (寒), Hot (热), Warm (温), Cool (凉), and Neutral (平). These describe the material\'s effect on the body\'s temperature balance.',
        'five_flavors': 'Five Flavors (五味):',
        'five_flavors_desc': 'Sour (酸), Bitter (苦), Sweet (甘), Spicy (辛), and Salty (咸). These flavors correspond to therapeutic actions and target organs.',
        'meridian_tropism': 'Meridian Tropism (归经):',
        'meridian_tropism_desc': 'Indicates which organ/meridian system the herb primarily affects, such as Lung, Liver, Heart, Spleen, Kidney, etc.',
        'distribution_help': 'Understanding these distributions helps practitioners create balanced prescriptions targeting specific conditions.',
        'five_properties_distribution': 'Five Properties Distribution (五性)',
        'five_flavors_distribution': 'Five Flavors Distribution (五味)',
        'meridian_distribution': 'Meridian Distribution (归经)',
        'no_property_data': 'No property data available. Please import medicinal material data with property information.',
        'no_flavor_data': 'No flavor data available. Please import medicinal material data with flavor information.',
        'no_meridian_data': 'No meridian data available. Please import medicinal material data with meridian information.',
        'property_flavor_meridian_data': 'Property, Flavor, and Meridian Data',
        'properties_tab': 'Properties',
        'flavors_tab': 'Flavors',
        'meridians_tab': 'Meridians',
        'property_column': 'Property',
        'flavor_column': 'Flavor',
        'meridian_column': 'Meridian',
        'count_column': 'Count',
        'percentage_column': 'Percentage',
        'no_data_available': 'No data available.',

        # Prescription related
        'add_prescription': 'Add New Prescription',
        'search_prescriptions': 'Search Prescriptions',
        'prescription_name': 'Prescription Name',
        'efficacy': 'Efficacy',
        'actions': 'Actions',
        'material_name': 'Material Name',
        'property': 'Property',
        'flavor': 'Flavor',
        'usage': 'Usage Count',
        'top_prescriptions': 'Top Prescriptions by Efficacy',
        'prescription_entry_instruction': 'Use this form to add a new prescription to the database. Be sure to include all required information and select the medicinal materials that comprise this prescription.',
        'prescription_name_help': 'Enter the traditional Chinese name of the prescription.',
        'description': 'Description',
        'description_help': 'Provide a brief description of the prescription\'s history and usage.',
        'efficacy_help': 'Describe what conditions this prescription is used to treat.',
        'efficacy_categories': 'Efficacy Categories',
        'efficacy_categories_help': 'Select existing categories or type new ones (separated by comma).',
        'medicinal_materials': 'Medicinal Materials',
        'materials_help': 'Select all materials that are part of this prescription.',
        'reset': 'Reset',
        'save_prescription': 'Save Prescription',
        'prescription_guidelines': 'Prescription Entry Guidelines',
        'required_information': 'Required Information:',
        'required_name': 'Prescription Name (in Chinese or transliteration)',
        'required_efficacy': 'Efficacy (conditions treated)',
        'required_material': 'At least one medicinal material',
        'helpful_tips': 'Helpful Tips:',
        'tip_description': 'Add detailed descriptions to improve searchability',
        'tip_categorize': 'Categorize prescriptions accurately for better analysis',
        'tip_materials': 'Include all materials, even those used in small amounts',
        'tip_preparation': 'Consider traditional preparation methods if relevant',
        'note': 'Note:',
        'material_not_in_list': 'If a medicinal material is not in the list, you must add it to the database first via the Data Import functionality.',

        # Top prescriptions page
        'top_prescriptions_for': 'Top Prescriptions for {0}',
        'select_category': 'Select Category',
        'top_prescriptions_by_efficacy': 'Top Prescriptions by Efficacy',
        'top_materials_for': 'Top Materials for {0}',
        'prescription': 'Prescription',
        'frequency': 'Frequency',
        'material': 'Material',

        # Prescription search page
        'search_criteria': 'Search Criteria',
        'search_by_name': 'Search by Name',
        'search_by_efficacy': 'Search by Efficacy',
        'search_by_material': 'Search by Material',
        'search_by_category': 'Search by Category',
        'search_results': 'Search Results',
        'no_results': 'No results found for your search criteria.',
        'property_label': 'Property',
        'flavor_label': 'Flavor',
        'meridian_label': 'Meridian',
        'efficacy_label': 'Efficacy',
        'categories_label': 'Categories',
        'no_description': 'No description available.',
        'no_materials': 'No materials found for this prescription.',
        'none_specified': 'None specified',
        'loading': 'Loading...',
        'network_error': 'Network response was not ok',
        'load_error': 'Failed to load prescription details. Please try again.',
        'medicinal_materials_heading': 'Medicinal Materials',
        'not_available': 'N/A',
        'search': 'Search',
        'clear': 'Clear',
        'view_details': 'View Details',
        'edit': 'Edit',
        'delete': 'Delete',

        # Formula optimization page
        'formula_optimization_intro': 'This tool uses machine learning to suggest optimized formulations based on your input.',
        'symptoms': 'Symptoms',
        'symptoms_help': 'Describe the symptoms or conditions you want to treat.',
        'base_materials': 'Base Materials',
        'base_materials_help': 'Select materials you want to include in the formula.',
        'optimize': 'Optimize',
        'optimization_results': 'Optimization Results',
        'suggested_formula': 'Suggested Formula',
        'confidence_score': 'Confidence Score',
        'similar_prescriptions': 'Similar Prescriptions',
        'recent_optimizations': 'Recent Optimizations',
        'date': 'Date',
        'symptoms_treated': 'Symptoms Treated',
        'no_optimization_results': 'No optimization results yet. Use the form to generate a suggested formula.',
        'no_recent_optimizations': 'No recent optimizations found.',
        'historical_data_analysis': 'Historical Data Analysis',
        'historical_data_analysis_desc': 'The system analyzes thousands of traditional prescriptions to identify patterns and relationships.',
        'machine_learning': 'Machine Learning',
        'machine_learning_desc': 'Advanced algorithms learn which materials work well together for specific conditions.',
        'property_balancing': 'Property Balancing',
        'property_balancing_desc': 'The system balances the five properties and flavors for harmonious formulations.',
        'interaction_analysis': 'Interaction Analysis',
        'interaction_analysis_desc': 'Potential synergistic and antagonistic interactions between materials are considered.',
        'optimization_algorithm_improvement': 'The optimization algorithm improves over time as more prescriptions and material data are added to the system.',

        # Knowledge graph page
        'knowledge_graph_intro': 'This visualization shows the relationships between medicinal materials, prescriptions, and their properties.',
        'graph_controls': 'Graph Controls',
        'show_materials': 'Show Materials',
        'show_prescriptions': 'Show Prescriptions',
        'show_properties': 'Show Properties',
        'show_flavors': 'Show Flavors',
        'show_meridians': 'Show Meridians',
        'zoom_in': 'Zoom In',
        'zoom_out': 'Zoom Out',
        'reset_view': 'Reset View',
        'search_graph': 'Search Graph',
        'loading_graph': 'Loading knowledge graph...',
        'graph_help': 'Click on nodes to see details. Drag nodes to rearrange the graph.',
        'material_nodes_description': 'Blue circles represent medicinal materials. Each material has properties, flavors, and meridian associations. The size of the node indicates how frequently it\'s used in prescriptions.',
        'prescription_nodes_description': 'Green circles represent prescriptions. These nodes connect to the materials they contain. The size of the node indicates the number of materials in the prescription.',
        'contains_relationships_description': 'Gray lines connect prescriptions to the materials they contain, showing the composition of each formula.',
        'interaction_relationships_description': 'Colored lines between materials indicate interactions:',
        'synergistic_interaction': 'Green: Synergistic (materials enhance each other)',
        'antagonistic_interaction': 'Red: Antagonistic (materials may counteract each other)',
        'other_interaction': 'Orange: Other interaction types',
        'formula_development': 'Formula Development',
        'formula_development_description': 'By analyzing the connections between materials and prescriptions, practitioners can identify common combinations and patterns that have proven effective, informing the development of new formulations.',
        'interaction_identification': 'Interaction Identification',
        'interaction_identification_description': 'The graph helps identify potential synergistic or antagonistic interactions between medicinal materials, which is crucial for safe and effective prescription formulation.',
        'knowledge_discovery': 'Knowledge Discovery',
        'knowledge_discovery_description': 'By exploring the graph, researchers can discover previously unknown relationships and patterns in traditional Chinese medicine, potentially leading to new therapeutic insights.',
        'educational_tool': 'Educational Tool',
        'educational_tool_description': 'The visual representation of connections between materials and prescriptions serves as a powerful educational tool for students learning about traditional Chinese medicine systems.',
        'medicinal_materials': 'Medicinal Materials',
        'material_name': 'Material Name'
    },
    'zh': {
        # Authentication
        'login': '登录',
        'register': '注册',
        'logout': '退出登录',
        'profile': '个人资料',
        'username': '用户名',
        'email': '电子邮箱',
        'password': '密码',
        'confirm_password': '确认密码',
        'current_password': '当前密码',
        'new_password': '新密码',
        'confirm_new_password': '确认新密码',
        'remember_me': '记住我',
        'forgot_password': '忘记密码？',
        'reset_password': '重置密码',
        'change_password': '修改密码',
        'update_password': '更新密码',
        'send_reset_link': '发送重置链接',
        'create_new_password': '为您的账户创建新密码。',
        'back_to_login': '返回登录',
        'login_success': '登录成功。',
        'login_failed': '登录失败。请检查您的用户名和密码。',
        'logout_success': '您已成功退出登录。',
        'register_success': '注册成功。',
        'register_failed': '注册失败。请重试。',
        'passwords_not_match': '密码不匹配。',
        'email_invalid': '无效的电子邮箱地址。',
        'username_exists': '用户名已存在。',
        'email_exists': '电子邮箱已存在。',
        'welcome_user': '欢迎，{}',
        'account_inactive': '您的账户已停用。请联系支持。',
        'login_required': '您需要登录才能访问此页面。',
        'admin_required': '您需要管理员权限才能访问此页面。',
        'email_verification': '电子邮箱验证',
        'verify_email': '验证电子邮箱',
        'verification_success': '电子邮箱验证成功！',
        'verification_failed': '验证失败',
        'verification_success_message': '您的电子邮箱已成功验证。您现在可以访问应用程序的所有功能。',
        'verification_failed_message': '验证链接无效或已过期。',
        'already_verified': '您的电子邮箱已经验证过了。',
        'verification_sent': '验证邮件已发送。请检查您的收件箱。',
        'email_required': '请输入您的电子邮箱地址。',
        'reset_password_sent': '如果您的电子邮箱地址存在于我们的数据库中，您将在几分钟内收到一封密码恢复链接邮件。',
        'reset_password_instructions': '输入您的电子邮箱地址，我们将向您发送重置密码的链接。',
        'invalid_token': '密码重置链接无效或已过期。',
        'password_required': '请输入新密码。',
        'password_reset_success': '您的密码已重置。您现在可以使用新密码登录。',
        'invalid_credentials': '用户名或密码无效。',
        'all_fields_required': '所有字段都是必填的。',
        'must_agree_terms': '您必须同意条款和条件。',
        'password_too_short': '密码长度必须至少为8个字符。',
        'current_password_incorrect': '当前密码不正确。',
        'password_changed': '您的密码已成功更改。',
        'preferences_updated': '您的偏好设置已更新。',
        'reset_link_sent': '密码重置链接已发送到您的电子邮箱。',
        'no_account': '还没有账户？',
        'register_now': '立即注册',
        'already_have_account': '已有账户？',
        'login_now': '立即登录',
        'agree_terms': '我同意条款和条件',
        'username_requirements': '用户名必须是3-20个字符长，只能包含字母、数字和下划线。',
        'password_requirements': '密码长度必须至少为8个字符。',
        'profile_info': '个人资料信息',
        'account_settings': '账户设置',
        'preferences': '偏好设置',
        'security': '安全',
        'activity': '活动',
        'language': '语言',
        'theme': '主题',
        'light': '浅色',
        'dark': '深色',
        'save_preferences': '保存偏好设置',
        'action': '操作',
        'timestamp': '时间戳',
        'details': '详情',
        'no_activity_records': '未找到活动记录。',
        'active_user': '活跃用户',
        'admin': '管理员',
        'member_since': '注册时间',
        'user_id': '用户ID',
        'no_account': '没有账户？',
        'already_have_account': '已有账户？',
        'account_info': '账户信息',
        'preferences': '偏好设置',
        'security': '安全',
        'activity_log': '活动日志',
        'no_activity_logs': '未找到活动日志。',
        'member_since': '注册时间',
        'last_login': '上次登录',
        'email_verified': '邮箱已验证',
        'email_not_verified': '邮箱未验证',
        'default_language': '默认语言',
        'theme': '主题',
        'light_theme': '浅色',
        'dark_theme': '深色',
        'enable_notifications': '启用通知',
        'save_changes': '保存更改',
        'action': '操作',
        'details': '详情',
        'ip_address': 'IP地址',
        'not_available': '无',
        # Import data page
        'import_data_description': '使用此表单将数据导入系统。您可以上传包含药材或处方信息的CSV文件。请确保您的文件遵循所需格式。',
        'import_type': '导入类型',
        'select_import_type': '选择导入类型',
        'csv_file': 'CSV文件',
        'upload_csv_instruction': '上传包含要导入数据的CSV文件。',
        'reset': '重置',
        'upload_and_process': '上传并处理',
        'recent_import_logs': '最近导入日志',
        'date': '日期',
        'filename': '文件名',
        'type': '类型',
        'rows_imported': '导入行数',
        'status': '状态',
        'success': '成功',
        'partial': '部分成功',
        'error': '错误',
        'import_errors': '导入错误',
        'close': '关闭',
        'no_import_logs': '未找到导入日志。开始导入一些数据。',
        'medicinal_materials_csv_format': '药材CSV格式',
        'materials_csv_description': '您的药材CSV文件应包含以下列：',
        'column': '列',
        'description': '描述',
        'required': '必填',
        'material_name_description': '药材名称',
        'pinyin_description': '拼音音译',
        'english_name_description': '药材的英文名称',
        'province_origin_description': '药材原产省份',
        'property_description': '五性（寒、热、温、凉、平）',
        'flavor_description': '五味（酸、苦、甘、辛、咸）',
        'meridian_description': '归经（影响哪个器官/经络）',
        'material_description_field': '药材描述',
        'yes': '是',
        'no': '否',
        'example': '示例',
        'prescriptions_csv_format': '处方CSV格式',
        'prescriptions_csv_description': '您的处方CSV文件应包含以下列：',
        'prescription_name_description': '处方名称',
        'prescription_description_field': '处方描述',
        'efficacy_description': '处方治疗的病症',
        'materials_format_description': '药材列表格式："名称1:用量1,名称2:用量2"',
        'efficacy_categories_description': '逗号分隔的功效类别列表',
        'note': '注意',
        'materials_prerequisite_warning': '在导入引用药材的处方之前，药材必须已存在于数据库中。',
        # Common elements
        'site_title': '中药处方分析系统',
        'dashboard': '仪表盘',
        'analytics': '分析',
        'prescriptions': '处方',
        'formula_optimization': '方剂优化',
        'knowledge_graph': '知识图谱',
        'import_data': '数据导入',
        'welcome': '欢迎使用中药处方分析系统',
        'welcome_description': '该平台提供分析传统中药处方、可视化药材使用模式以及基于机器学习优化配方的工具。',

        # Dashboard statistics
        'medicinal_materials': '药材',
        'prescription_formulas': '处方方剂',
        'efficacy_categories': '功效分类',
        'recent_prescriptions': '最近处方',
        'top_materials': '常用药材',
        'view_all': '查看全部',
        'quick_analysis': '快速分析',
        'no_prescriptions': '未找到处方。添加处方以开始使用。',
        'no_materials': '未找到药材。导入数据以开始使用。',

        # Province stats page
        'province_stats': '各省统计',
        'materials_by_province': '各省药材分布',
        'province_stats_description': '此可视化展示了中国各省生产的药材分布情况。了解区域生产模式有助于分析中药资源的地理特征。',

        # Material usage page
        'material_usage': '药材使用情况',
        'usage_frequency': '使用频率',
        'usage_distribution': '使用分布',
        'usage_frequency_description': '此可视化展示了数据库中所有处方中各种药材的使用频率。出现频率较高的药材通常是传统中医药中的重要组成部分。',
        'material_usage_distribution': '药材使用分布',
        'material_usage_insights': '药材使用洞察',
        'key_insights': '关键洞察：',
        'insight_1': '使用最多的药材通常表明传统配方中的核心成分',
        'insight_2': '使用频率高的药材通常具有广泛的治疗应用',
        'insight_3': '了解使用模式有助于优化新配方',
        'insight_4': '区域差异可能影响药材可用性和处方定制',
        'tip': '提示：',
        'usage_tip': '将药材使用情况与功效类别进行比较，以确定特定病症的专用药材。',
        'view_top_prescriptions': '查看常用处方',
        'material_clustering': '药材聚类',
        'clustering_description': '此可视化根据药材的性质、味道和使用模式对药材进行聚类。相似的药材被分组在一起，揭示了中医药理学中的自然分类。',

        # Property distribution page
        'property_distribution': '性味归经分布',
        'tcm_attributes_intro': '在传统中医中，药材按三个关键属性分类：',
        'five_properties': '五性：',
        'five_properties_desc': '寒、热、温、凉和平。这些描述了药材对身体温度平衡的影响。',
        'five_flavors': '五味：',
        'five_flavors_desc': '酸、苦、甘、辛和咸。这些味道对应于治疗作用和靶器官。',
        'meridian_tropism': '归经：',
        'meridian_tropism_desc': '表示药材主要影响哪个器官/经络系统，如肺、肝、心、脾、肾等。',
        'distribution_help': '了解这些分布有助于医生创建针对特定病症的平衡处方。',
        'five_properties_distribution': '五性分布',
        'five_flavors_distribution': '五味分布',
        'meridian_distribution': '归经分布',
        'no_property_data': '没有可用的性质数据。请导入带有性质信息的药材数据。',
        'no_flavor_data': '没有可用的味道数据。请导入带有味道信息的药材数据。',
        'no_meridian_data': '没有可用的归经数据。请导入带有归经信息的药材数据。',
        'property_flavor_meridian_data': '性味归经数据',
        'properties_tab': '性质',
        'flavors_tab': '味道',
        'meridians_tab': '归经',
        'property_column': '性质',
        'flavor_column': '味道',
        'meridian_column': '归经',
        'count_column': '数量',
        'percentage_column': '百分比',
        'no_data_available': '没有可用数据。',

        # Prescription related
        'add_prescription': '添加新处方',
        'search_prescriptions': '搜索处方',
        'prescription_name': '处方名称',
        'efficacy': '功效',
        'actions': '操作',
        'material_name': '药材名称',
        'property': '性质',
        'flavor': '味道',
        'usage': '使用次数',
        'top_prescriptions': '按功效分类的常用处方',
        'prescription_entry_instruction': '使用此表格将新处方添加到数据库。请确保包含所有必要信息并选择构成此处方的药材。',
        'prescription_name_help': '输入处方的传统中文名称。',
        'description': '描述',
        'description_help': '提供处方历史和用途的简要描述。',
        'efficacy_help': '描述此处方用于治疗的病症。',
        'efficacy_categories': '功效分类',
        'efficacy_categories_help': '选择现有类别或输入新类别（用逗号分隔）。',
        'medicinal_materials': '药材',
        'materials_help': '选择构成此处方的所有药材。',
        'reset': '重置',
        'save_prescription': '保存处方',
        'prescription_guidelines': '处方录入指南',
        'required_information': '必填信息：',
        'required_name': '处方名称（中文或音译）',
        'required_efficacy': '功效（治疗的病症）',
        'required_material': '至少一种药材',
        'helpful_tips': '有用的提示：',
        'tip_description': '添加详细描述以提高可搜索性',
        'tip_categorize': '准确分类处方以便于更好的分析',
        'tip_materials': '包含所有药材，即使是少量使用的',
        'tip_preparation': '如果相关，考虑传统的制备方法',
        'note': '注意：',
        'material_not_in_list': '如果列表中没有某种药材，您必须先通过数据导入功能将其添加到数据库中。',

        # Top prescriptions page
        'top_prescriptions_for': '{0}的常用处方',
        'select_category': '选择类别',
        'top_prescriptions_by_efficacy': '按功效分类的常用处方',
        'top_materials_for': '{0}的常用药材',
        'prescription': '处方',
        'frequency': '频率',
        'material': '药材',

        # Prescription search page
        'search_criteria': '搜索条件',
        'search_by_name': '按名称搜索',
        'search_by_efficacy': '按功效搜索',
        'search_by_material': '按药材搜索',
        'search_by_category': '按类别搜索',
        'search_results': '搜索结果',
        'no_results': '没有找到符合您搜索条件的结果。',
        'property_label': '性质',
        'flavor_label': '味道',
        'meridian_label': '归经',
        'efficacy_label': '功效',
        'categories_label': '分类',
        'no_description': '暂无描述。',
        'no_materials': '未找到该处方的药材。',
        'none_specified': '未指定',
        'loading': '加载中...',
        'network_error': '网络响应异常',
        'load_error': '加载处方详情失败。请重试。',
        'medicinal_materials_heading': '药材',
        'not_available': '无',
        'search': '搜索',
        'clear': '清除',
        'view_details': '查看详情',
        'edit': '编辑',
        'delete': '删除',

        # Formula optimization page
        'formula_optimization_intro': '此工具使用机器学习根据您的输入推荐优化的配方。',
        'symptoms': '症状',
        'symptoms_help': '描述您想要治疗的症状或病症。',
        'base_materials': '基础药材',
        'base_materials_help': '选择您想要包含在配方中的药材。',
        'optimize': '优化',
        'optimization_results': '优化结果',
        'suggested_formula': '建议的配方',
        'confidence_score': '置信度评分',
        'similar_prescriptions': '类似处方',
        'recent_optimizations': '最近的优化',
        'date': '日期',
        'symptoms_treated': '治疗的症状',
        'no_optimization_results': '还没有优化结果。使用表格生成建议的配方。',
        'no_recent_optimizations': '没有找到最近的优化。',
        'historical_data_analysis': '历史数据分析',
        'historical_data_analysis_desc': '系统分析成千上万的传统处方，以识别模式和关系。',
        'machine_learning': '机器学习',
        'machine_learning_desc': '高级算法学习哪些药材对特定病症有效地协同工作。',
        'property_balancing': '性味平衡',
        'property_balancing_desc': '系统平衡五性和五味，以达到和谐的配方。',
        'interaction_analysis': '相互作用分析',
        'interaction_analysis_desc': '考虑药材之间潜在的协同和拮抗相互作用。',
        'optimization_algorithm_improvement': '优化算法会随着更多处方和药材数据添加到系统中而不断改进。',

        # Knowledge graph page
        'knowledge_graph_intro': '此可视化显示药材、处方及其属性之间的关系。',
        'graph_controls': '图表控制',
        'show_materials': '显示药材',
        'show_prescriptions': '显示处方',
        'show_properties': '显示性质',
        'show_flavors': '显示味道',
        'show_meridians': '显示归经',
        'zoom_in': '放大',
        'zoom_out': '缩小',
        'reset_view': '重置视图',
        'search_graph': '搜索图表',
        'loading_graph': '正在加载知识图谱...',
        'graph_help': '点击节点查看详情。拖动节点重新排列图表。',
        'material_nodes_description': '蓝色圆圈代表药材。每种药材都有性质、味道和归经关联。节点的大小表示它在处方中使用的频率。',
        'prescription_nodes_description': '绿色圆圈代表处方。这些节点连接到它们包含的药材。节点的大小表示处方中药材的数量。',
        'contains_relationships_description': '灰色线条连接处方与其包含的药材，显示每个方剂的组成。',
        'interaction_relationships_description': '药材之间的彩色线条表示相互作用：',
        'synergistic_interaction': '绿色：协同作用（药材相互增强）',
        'antagonistic_interaction': '红色：拮抗作用（药材可能相互抵消）',
        'other_interaction': '橙色：其他相互作用类型',
        'formula_development': '方剂开发',
        'formula_development_description': '通过分析药材和处方之间的联系，医生可以识别已被证明有效的常见组合和模式，为新方剂的开发提供信息。',
        'interaction_identification': '相互作用识别',
        'interaction_identification_description': '图谱有助于识别药材之间潜在的协同或拮抗相互作用，这对于安全有效的处方配方至关重要。',
        'knowledge_discovery': '知识发现',
        'knowledge_discovery_description': '通过探索图谱，研究人员可以发现传统中医中以前未知的关系和模式，可能导致新的治疗见解。',
        'educational_tool': '教育工具',
        'educational_tool_description': '药材和处方之间联系的可视化表示为学习传统中医系统的学生提供了强大的教育工具。',
        'medicinal_materials': '药材',
        'material_name': '药材名称'
    }
}

def get_text(key, lang='en', *args):
    """
    Get translated text for a given key and language

    Args:
        key (str): Translation key
        lang (str): Language code ('en' or 'zh')
        *args: Optional arguments for string formatting

    Returns:
        str: Translated text
    """
    if lang not in translations:
        lang = 'en'

    text = translations[lang].get(key, translations['en'].get(key, key))

    if args:
        try:
            text = text.format(*args)
        except:
            pass

    return text