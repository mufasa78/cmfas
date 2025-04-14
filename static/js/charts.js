/**
 * Charts.js - Handles all chart rendering for the application
 */

// Initialize ECharts instances for different charts
let provinceChart = null;
let materialUsageChart = null;
let propertyChart = null;
let flavorChart = null;
let meridianChart = null;
let topMaterialsChart = null;

/**
 * Initializes the province statistics chart
 * @param {string} elementId - DOM element ID for the chart
 * @param {Object} data - Province statistics data
 */
function initProvinceChart(elementId, data) {
    // Check if chart instance already exists
    if (provinceChart) {
        provinceChart.dispose();
    }

    // Initialize chart with light theme
    provinceChart = echarts.init(document.getElementById(elementId), 'light-theme');

    // Convert data to array format for ECharts
    const provinces = Object.keys(data);
    const values = provinces.map(province => data[province]);

    // Create dataset for sorting
    const dataset = provinces.map((province, index) => ({
        province: province,
        value: values[index]
    }));

    // Sort dataset by value in descending order
    dataset.sort((a, b) => b.value - a.value);

    // Create sorted arrays
    const sortedProvinces = dataset.map(item => item.province);
    const sortedValues = dataset.map(item => item.value);

    // Configure chart options
    const options = {
        title: {
            text: 'Medicinal Materials by Province',
            left: 'center',
            textStyle: {
                color: '#333'
            }
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            },
            formatter: '{b}: {c}'
        },
        grid: {
            left: '5%',
            right: '5%',
            bottom: '15%',
            containLabel: true
        },
        xAxis: {
            type: 'category',
            data: sortedProvinces,
            axisLabel: {
                interval: 0,
                rotate: 45,
                color: '#333'
            },
            axisLine: {
                lineStyle: {
                    color: '#333'
                }
            }
        },
        yAxis: {
            type: 'value',
            name: 'Number of Materials',
            nameTextStyle: {
                color: '#333'
            },
            axisLabel: {
                color: '#333'
            },
            axisLine: {
                lineStyle: {
                    color: '#333'
                }
            }
        },
        series: [
            {
                name: 'Materials',
                type: 'bar',
                data: sortedValues,
                itemStyle: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        { offset: 0, color: '#83bff6' },
                        { offset: 0.5, color: '#188df0' },
                        { offset: 1, color: '#188df0' }
                    ])
                },
                emphasis: {
                    itemStyle: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                            { offset: 0, color: '#2378f7' },
                            { offset: 0.7, color: '#2378f7' },
                            { offset: 1, color: '#83bff6' }
                        ])
                    }
                }
            }
        ]
    };

    // Set options and render chart
    provinceChart.setOption(options);

    // Add resize event listener
    window.addEventListener('resize', () => {
        provinceChart.resize();
    });
}

/**
 * Initializes the material usage frequency chart
 * @param {string} elementId - DOM element ID for the chart
 */
function initMaterialUsageChart(elementId) {
    // Check if chart instance already exists
    if (materialUsageChart) {
        materialUsageChart.dispose();
    }

    // Initialize chart with light theme
    materialUsageChart = echarts.init(document.getElementById(elementId), 'light-theme');

    // Show loading animation first
    materialUsageChart.showLoading();

    // Fetch material usage data
    fetch('/api/material-usage')
        .then(response => response.json())
        .then(data => {
            // Hide loading animation
            materialUsageChart.hideLoading();

            // Limit to top 20 for better visualization
            const limitedData = data.slice(0, 20);

            // Configure chart options
            const options = {
                title: {
                    text: 'Top 20 Medicinal Materials by Usage Frequency',
                    left: 'center',
                    textStyle: {
                        color: '#333'
                    }
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'shadow'
                    }
                },
                legend: {
                    data: ['Usage Frequency'],
                    bottom: 10,
                    textStyle: {
                        color: '#333'
                    }
                },
                grid: {
                    left: '5%',
                    right: '5%',
                    bottom: '15%',
                    containLabel: true
                },
                xAxis: {
                    type: 'category',
                    data: limitedData.map(item => item.name),
                    axisLabel: {
                        interval: 0,
                        rotate: 45,
                        color: '#333'
                    },
                    axisLine: {
                        lineStyle: {
                            color: '#333'
                        }
                    }
                },
                yAxis: {
                    type: 'value',
                    name: 'Frequency',
                    nameTextStyle: {
                        color: '#333'
                    },
                    axisLabel: {
                        color: '#333'
                    },
                    axisLine: {
                        lineStyle: {
                            color: '#333'
                        }
                    }
                },
                series: [
                    {
                        name: 'Usage Frequency',
                        type: 'bar',
                        data: limitedData.map(item => item.value),
                        itemStyle: {
                            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                                { offset: 0, color: '#f7a35c' },
                                { offset: 0.5, color: '#e9632c' },
                                { offset: 1, color: '#e9632c' }
                            ])
                        },
                        emphasis: {
                            itemStyle: {
                                color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                                    { offset: 0, color: '#ff7c1f' },
                                    { offset: 0.7, color: '#ff7c1f' },
                                    { offset: 1, color: '#f7a35c' }
                                ])
                            }
                        }
                    }
                ]
            };

            // Set options and render chart
            materialUsageChart.setOption(options);
        })
        .catch(error => {
            console.error('Error fetching material usage data:', error);
            materialUsageChart.hideLoading();
            materialUsageChart.setOption({
                title: {
                    text: 'Error Loading Data',
                    left: 'center',
                    textStyle: {
                        color: '#f56c6c'
                    }
                }
            });
        });

    // Add resize event listener
    window.addEventListener('resize', () => {
        materialUsageChart.resize();
    });
}

/**
 * Initializes the material usage pie chart
 * @param {string} elementId - DOM element ID for the chart
 */
function initMaterialUsagePieChart(elementId) {
    // Check if chart instance already exists
    const chartElement = document.getElementById(elementId);
    if (!chartElement) return;

    const pieChart = echarts.init(chartElement, 'light-theme');

    // Show loading animation first
    pieChart.showLoading();

    // Fetch material usage data
    fetch('/api/material-usage')
        .then(response => response.json())
        .then(data => {
            // Hide loading animation
            pieChart.hideLoading();

            // Limit to top 10 for better pie chart visualization
            const limitedData = data.slice(0, 10);

            // Configure chart options
            const options = {
                title: {
                    text: 'Top 10 Medicinal Materials',
                    left: 'center',
                    textStyle: {
                        color: '#333'
                    }
                },
                tooltip: {
                    trigger: 'item',
                    formatter: '{a} <br/>{b}: {c} ({d}%)'
                },
                legend: {
                    orient: 'vertical',
                    left: 10,
                    top: 'middle',
                    data: limitedData.map(item => item.name),
                    textStyle: {
                        color: '#333'
                    }
                },
                series: [
                    {
                        name: 'Usage Frequency',
                        type: 'pie',
                        radius: ['40%', '70%'],
                        avoidLabelOverlap: false,
                        itemStyle: {
                            borderRadius: 10,
                            borderColor: '#fff',
                            borderWidth: 2
                        },
                        label: {
                            show: false,
                            position: 'center'
                        },
                        emphasis: {
                            label: {
                                show: true,
                                fontSize: '16',
                                fontWeight: 'bold'
                            }
                        },
                        labelLine: {
                            show: false
                        },
                        data: limitedData.map(item => ({
                            name: item.name,
                            value: item.value
                        }))
                    }
                ]
            };

            // Set options and render chart
            pieChart.setOption(options);
        })
        .catch(error => {
            console.error('Error fetching material usage data:', error);
            pieChart.hideLoading();
            pieChart.setOption({
                title: {
                    text: 'Error Loading Data',
                    left: 'center',
                    textStyle: {
                        color: '#f56c6c'
                    }
                }
            });
        });

    // Add resize event listener
    window.addEventListener('resize', () => {
        pieChart.resize();
    });
}

/**
 * Initializes the property distribution pie chart
 * @param {string} elementId - DOM element ID for the chart
 * @param {Object} data - Property distribution data
 */
function initPropertyChart(elementId, data) {
    // Check if chart instance already exists
    if (propertyChart) {
        propertyChart.dispose();
    }

    // Initialize chart with light theme
    propertyChart = echarts.init(document.getElementById(elementId), 'light-theme');

    // Convert data to array format for ECharts
    const properties = Object.keys(data);
    const pieData = properties.map(property => ({
        name: property,
        value: data[property]
    }));

    // Configure chart options
    const options = {
        title: {
            text: 'Distribution of Five Properties (五性)',
            left: 'center',
            textStyle: {
                color: '#333'
            }
        },
        tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        legend: {
            orient: 'vertical',
            left: 10,
            top: 'middle',
            data: properties,
            textStyle: {
                color: '#333'
            }
        },
        series: [
            {
                name: 'Property',
                type: 'pie',
                radius: ['50%', '70%'],
                avoidLabelOverlap: false,
                itemStyle: {
                    borderRadius: 10,
                    borderColor: '#fff',
                    borderWidth: 2
                },
                label: {
                    show: false,
                    position: 'center'
                },
                emphasis: {
                    label: {
                        show: true,
                        fontSize: '16',
                        fontWeight: 'bold'
                    }
                },
                labelLine: {
                    show: false
                },
                data: pieData
            }
        ],
        color: ['#dd6b66', '#759aa0', '#e69d87', '#8dc1a9', '#ea7e53']
    };

    // Set options and render chart
    propertyChart.setOption(options);

    // Add resize event listener
    window.addEventListener('resize', () => {
        propertyChart.resize();
    });
}

/**
 * Initializes the flavor distribution pie chart
 * @param {string} elementId - DOM element ID for the chart
 * @param {Object} data - Flavor distribution data
 */
function initFlavorChart(elementId, data) {
    // Check if chart instance already exists
    if (flavorChart) {
        flavorChart.dispose();
    }

    // Initialize chart with light theme
    flavorChart = echarts.init(document.getElementById(elementId), 'light-theme');

    // Convert data to array format for ECharts
    const flavors = Object.keys(data);
    const pieData = flavors.map(flavor => ({
        name: flavor,
        value: data[flavor]
    }));

    // Configure chart options
    const options = {
        title: {
            text: 'Distribution of Five Flavors (五味)',
            left: 'center',
            textStyle: {
                color: '#333'
            }
        },
        tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        legend: {
            orient: 'vertical',
            left: 10,
            top: 'middle',
            data: flavors,
            textStyle: {
                color: '#333'
            }
        },
        series: [
            {
                name: 'Flavor',
                type: 'pie',
                radius: ['50%', '70%'],
                avoidLabelOverlap: false,
                itemStyle: {
                    borderRadius: 10,
                    borderColor: '#fff',
                    borderWidth: 2
                },
                label: {
                    show: false,
                    position: 'center'
                },
                emphasis: {
                    label: {
                        show: true,
                        fontSize: '16',
                        fontWeight: 'bold'
                    }
                },
                labelLine: {
                    show: false
                },
                data: pieData
            }
        ],
        color: ['#73c0de', '#5470c6', '#91cc75', '#fac858', '#ee6666']
    };

    // Set options and render chart
    flavorChart.setOption(options);

    // Add resize event listener
    window.addEventListener('resize', () => {
        flavorChart.resize();
    });
}

/**
 * Initializes the meridian distribution chart
 * @param {string} elementId - DOM element ID for the chart
 * @param {Object} data - Meridian distribution data
 */
function initMeridianChart(elementId, data) {
    // Check if chart instance already exists
    if (meridianChart) {
        meridianChart.dispose();
    }

    // Initialize chart with light theme
    meridianChart = echarts.init(document.getElementById(elementId), 'light-theme');

    // Convert data to array format for ECharts and sort
    const meridians = Object.keys(data);
    const dataset = meridians.map(meridian => ({
        meridian: meridian,
        value: data[meridian]
    }));

    // Sort by value in descending order
    dataset.sort((a, b) => b.value - a.value);

    // Create sorted arrays
    const sortedMeridians = dataset.map(item => item.meridian);
    const sortedValues = dataset.map(item => item.value);

    // Configure chart options
    const options = {
        title: {
            text: 'Distribution of Meridians (归经)',
            left: 'center',
            textStyle: {
                color: '#333'
            }
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        grid: {
            left: '5%',
            right: '5%',
            bottom: '15%',
            containLabel: true
        },
        xAxis: {
            type: 'category',
            data: sortedMeridians,
            axisLabel: {
                interval: 0,
                rotate: 45,
                color: '#333'
            },
            axisLine: {
                lineStyle: {
                    color: '#333'
                }
            }
        },
        yAxis: {
            type: 'value',
            name: 'Count',
            nameTextStyle: {
                color: '#333'
            },
            axisLabel: {
                color: '#333'
            },
            axisLine: {
                lineStyle: {
                    color: '#333'
                }
            }
        },
        series: [
            {
                name: 'Meridian',
                type: 'bar',
                data: sortedValues,
                itemStyle: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        { offset: 0, color: '#91cc75' },
                        { offset: 0.5, color: '#5ab34b' },
                        { offset: 1, color: '#5ab34b' }
                    ])
                },
                emphasis: {
                    itemStyle: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                            { offset: 0, color: '#5ab34b' },
                            { offset: 0.7, color: '#5ab34b' },
                            { offset: 1, color: '#91cc75' }
                        ])
                    }
                }
            }
        ]
    };

    // Set options and render chart
    meridianChart.setOption(options);

    // Add resize event listener
    window.addEventListener('resize', () => {
        meridianChart.resize();
    });
}

/**
 * Initializes the top materials by efficacy chart
 * @param {string} elementId - DOM element ID for the chart
 * @param {Array} data - Top materials data
 */
function initTopMaterialsChart(elementId, data) {
    // Check if chart instance already exists
    if (topMaterialsChart) {
        topMaterialsChart.dispose();
    }

    // Initialize chart with light theme
    topMaterialsChart = echarts.init(document.getElementById(elementId), 'light-theme');

    // Sort data by count in descending order
    data.sort((a, b) => b.count - a.count);

    // Configure chart options
    const options = {
        title: {
            text: 'Top Medicinal Materials by Efficacy',
            left: 'center',
            textStyle: {
                color: '#333'
            }
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        grid: {
            left: '5%',
            right: '5%',
            bottom: '15%',
            containLabel: true
        },
        xAxis: {
            type: 'category',
            data: data.map(item => item.name),
            axisLabel: {
                interval: 0,
                rotate: 45,
                color: '#333'
            },
            axisLine: {
                lineStyle: {
                    color: '#333'
                }
            }
        },
        yAxis: {
            type: 'value',
            name: 'Count',
            nameTextStyle: {
                color: '#333'
            },
            axisLabel: {
                color: '#333'
            },
            axisLine: {
                lineStyle: {
                    color: '#333'
                }
            }
        },
        series: [
            {
                type: 'bar',
                data: data.map(item => item.count),
                itemStyle: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        { offset: 0, color: '#67e0e3' },
                        { offset: 0.5, color: '#37a2da' },
                        { offset: 1, color: '#37a2da' }
                    ])
                },
                emphasis: {
                    itemStyle: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                            { offset: 0, color: '#37a2da' },
                            { offset: 0.7, color: '#37a2da' },
                            { offset: 1, color: '#67e0e3' }
                        ])
                    }
                }
            }
        ]
    };

    // Set options and render chart
    topMaterialsChart.setOption(options);

    // Add resize event listener
    window.addEventListener('resize', () => {
        topMaterialsChart.resize();
    });
}

/**
 * Initializes the material clustering visualization
 * @param {string} elementId - DOM element ID for the chart
 */
function initMaterialClustering(elementId) {
    const chart = echarts.init(document.getElementById(elementId), 'light-theme');

    // Show loading animation first
    chart.showLoading();

    // Fetch clustering data
    fetch('/api/material-clusters')
        .then(response => response.json())
        .then(data => {
            // Hide loading animation
            chart.hideLoading();

            if (!data.success) {
                chart.setOption({
                    title: {
                        text: 'Error: ' + (data.message || 'Unable to generate clusters'),
                        left: 'center',
                        textStyle: {
                            color: '#f56c6c'
                        }
                    }
                });
                return;
            }

            const clusters = data.clusters;
            const series = [];

            // Create a series for each cluster
            clusters.forEach(cluster => {
                series.push({
                    name: `Cluster ${cluster.cluster_id + 1}: ${cluster.common_properties}/${cluster.common_flavors}`,
                    type: 'scatter',
                    symbolSize: function(data) {
                        // Size based on usage frequency (min 5, max 20)
                        return Math.max(5, Math.min(20, 5 + data[2] / 5));
                    },
                    data: cluster.materials.map(m => [m.x, m.y, m.usage_frequency, m.name]),
                    emphasis: {
                        focus: 'series',
                        label: {
                            show: true,
                            formatter: function(param) {
                                return param.data[3];
                            },
                            position: 'top'
                        }
                    }
                });
            });

            // Configure chart options
            const options = {
                title: {
                    text: 'Material Clustering by Properties',
                    left: 'center',
                    textStyle: {
                        color: '#333'
                    }
                },
                tooltip: {
                    trigger: 'item',
                    formatter: function(param) {
                        const data = param.data;
                        return `${data[3]}<br/>Usage: ${data[2]}<br/>Cluster: ${param.seriesName}`;
                    }
                },
                legend: {
                    data: series.map(s => s.name),
                    bottom: 10,
                    textStyle: {
                        color: '#333'
                    }
                },
                grid: {
                    left: '5%',
                    right: '5%',
                    bottom: '15%',
                    containLabel: true
                },
                xAxis: {
                    type: 'value',
                    name: 'Component 1',
                    nameTextStyle: {
                        color: '#333'
                    },
                    axisLabel: {
                        color: '#333'
                    },
                    axisLine: {
                        lineStyle: {
                            color: '#333'
                        }
                    },
                    splitLine: {
                        lineStyle: {
                            color: 'rgba(204, 204, 204, 0.5)'
                        }
                    }
                },
                yAxis: {
                    type: 'value',
                    name: 'Component 2',
                    nameTextStyle: {
                        color: '#333'
                    },
                    axisLabel: {
                        color: '#333'
                    },
                    axisLine: {
                        lineStyle: {
                            color: '#333'
                        }
                    },
                    splitLine: {
                        lineStyle: {
                            color: 'rgba(204, 204, 204, 0.5)'
                        }
                    }
                },
                series: series
            };

            // Set options and render chart
            chart.setOption(options);
        })
        .catch(error => {
            console.error('Error fetching clustering data:', error);
            chart.hideLoading();
            chart.setOption({
                title: {
                    text: 'Error Loading Clustering Data',
                    left: 'center',
                    textStyle: {
                        color: '#f56c6c'
                    }
                }
            });
        });

    // Add resize event listener
    window.addEventListener('resize', () => {
        chart.resize();
    });
}
