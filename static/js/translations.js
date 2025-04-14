/**
 * Translations.js - Handles translations for dynamic content
 */

// Global translations object
const translations = {
    en: {
        property_label: 'Property',
        flavor_label: 'Flavor',
        meridian_label: 'Meridian',
        efficacy_label: 'Efficacy',
        categories_label: 'Categories',
        no_description: 'No description available.',
        no_materials: 'No materials found for this prescription.',
        none_specified: 'None specified',
        loading: 'Loading...',
        network_error: 'Network response was not ok',
        load_error: 'Failed to load prescription details. Please try again.',
        medicinal_materials_heading: 'Medicinal Materials',
        not_available: 'N/A',
        select_medicinal_materials: 'Select medicinal materials',
        enter_efficacy_categories: 'Enter efficacy categories',
        select_a_medicinal_material: 'Select a medicinal material',
        select_an_efficacy_category: 'Select an efficacy category',
        select_base_materials: 'Select base materials (optional)'
    },
    zh: {
        property_label: '性质',
        flavor_label: '味道',
        meridian_label: '归经',
        efficacy_label: '功效',
        categories_label: '分类',
        no_description: '暂无描述。',
        no_materials: '未找到该处方的药材。',
        none_specified: '未指定',
        loading: '加载中...',
        network_error: '网络响应异常',
        load_error: '加载处方详情失败。请重试。',
        medicinal_materials_heading: '药材',
        not_available: '无',
        select_medicinal_materials: '选择药材',
        enter_efficacy_categories: '输入功效分类',
        select_a_medicinal_material: '选择一种药材',
        select_an_efficacy_category: '选择一个功效分类',
        select_base_materials: '选择基础药材（可选）'
    }
};

/**
 * Get translated text based on current language
 * @param {string} key - Translation key
 * @returns {string} - Translated text
 */
function getTranslation(key) {
    // Get current language from html lang attribute or default to English
    const lang = document.documentElement.lang || 'en';

    // Return translation or key if not found
    return (translations[lang] && translations[lang][key]) ||
           (translations['en'] && translations['en'][key]) ||
           key;
}

// Export for use in other scripts
window.getTranslation = getTranslation;
