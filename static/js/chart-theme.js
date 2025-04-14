/**
 * Chart theme configuration for light mode
 * This file sets up a light theme for all charts in the application
 */

// Register a light theme for ECharts
echarts.registerTheme('light-theme', {
    // Color palette
    color: [
        '#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de',
        '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc'
    ],
    
    // Global text style
    textStyle: {
        color: '#333'
    },
    
    // Title text style
    title: {
        textStyle: {
            color: '#333'
        },
        subtextStyle: {
            color: '#666'
        }
    },
    
    // Line style
    line: {
        itemStyle: {
            borderWidth: 1
        },
        lineStyle: {
            width: 2
        },
        symbolSize: 4,
        symbol: 'emptyCircle',
        smooth: false
    },
    
    // Radar chart style
    radar: {
        itemStyle: {
            borderWidth: 1
        },
        lineStyle: {
            width: 2
        },
        symbolSize: 4,
        symbol: 'emptyCircle',
        smooth: false
    },
    
    // Bar chart style
    bar: {
        itemStyle: {
            barBorderWidth: 0,
            barBorderColor: '#ccc'
        }
    },
    
    // Pie chart style
    pie: {
        itemStyle: {
            borderWidth: 0,
            borderColor: '#ccc'
        }
    },
    
    // Scatter chart style
    scatter: {
        itemStyle: {
            borderWidth: 0,
            borderColor: '#ccc'
        }
    },
    
    // Box plot style
    boxplot: {
        itemStyle: {
            borderWidth: 0,
            borderColor: '#ccc'
        }
    },
    
    // Parallel style
    parallel: {
        itemStyle: {
            borderWidth: 0,
            borderColor: '#ccc'
        }
    },
    
    // Sankey diagram style
    sankey: {
        itemStyle: {
            borderWidth: 0,
            borderColor: '#ccc'
        }
    },
    
    // Funnel chart style
    funnel: {
        itemStyle: {
            borderWidth: 0,
            borderColor: '#ccc'
        }
    },
    
    // Gauge style
    gauge: {
        itemStyle: {
            borderWidth: 0,
            borderColor: '#ccc'
        }
    },
    
    // Candlestick style
    candlestick: {
        itemStyle: {
            color: '#eb5454',
            color0: '#47b262',
            borderColor: '#eb5454',
            borderColor0: '#47b262',
            borderWidth: 1
        }
    },
    
    // Graph style
    graph: {
        itemStyle: {
            borderWidth: 0,
            borderColor: '#ccc'
        },
        lineStyle: {
            width: 1,
            color: '#aaa'
        },
        symbolSize: 4,
        symbol: 'emptyCircle',
        smooth: false,
        color: [
            '#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de',
            '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc'
        ],
        label: {
            color: '#333'
        }
    },
    
    // Map style
    map: {
        itemStyle: {
            areaColor: '#eee',
            borderColor: '#444',
            borderWidth: 0.5
        },
        label: {
            color: '#000'
        },
        emphasis: {
            itemStyle: {
                areaColor: 'rgba(255,215,0,0.8)',
                borderColor: '#444',
                borderWidth: 1
            },
            label: {
                color: '#000'
            }
        }
    },
    
    // Geo style
    geo: {
        itemStyle: {
            areaColor: '#eee',
            borderColor: '#444',
            borderWidth: 0.5
        },
        label: {
            color: '#000'
        },
        emphasis: {
            itemStyle: {
                areaColor: 'rgba(255,215,0,0.8)',
                borderColor: '#444',
                borderWidth: 1
            },
            label: {
                color: '#000'
            }
        }
    },
    
    // Category axis
    categoryAxis: {
        axisLine: {
            show: true,
            lineStyle: {
                color: '#333'
            }
        },
        axisTick: {
            show: true,
            lineStyle: {
                color: '#333'
            }
        },
        axisLabel: {
            show: true,
            color: '#333'
        },
        splitLine: {
            show: false,
            lineStyle: {
                color: [
                    '#ccc'
                ]
            }
        },
        splitArea: {
            show: false,
            areaStyle: {
                color: [
                    'rgba(250,250,250,0.3)',
                    'rgba(200,200,200,0.3)'
                ]
            }
        }
    },
    
    // Value axis
    valueAxis: {
        axisLine: {
            show: true,
            lineStyle: {
                color: '#333'
            }
        },
        axisTick: {
            show: true,
            lineStyle: {
                color: '#333'
            }
        },
        axisLabel: {
            show: true,
            color: '#333'
        },
        splitLine: {
            show: true,
            lineStyle: {
                color: [
                    '#ccc'
                ]
            }
        },
        splitArea: {
            show: false,
            areaStyle: {
                color: [
                    'rgba(250,250,250,0.3)',
                    'rgba(200,200,200,0.3)'
                ]
            }
        }
    },
    
    // Log axis
    logAxis: {
        axisLine: {
            show: true,
            lineStyle: {
                color: '#333'
            }
        },
        axisTick: {
            show: true,
            lineStyle: {
                color: '#333'
            }
        },
        axisLabel: {
            show: true,
            color: '#333'
        },
        splitLine: {
            show: true,
            lineStyle: {
                color: [
                    '#ccc'
                ]
            }
        },
        splitArea: {
            show: false,
            areaStyle: {
                color: [
                    'rgba(250,250,250,0.3)',
                    'rgba(200,200,200,0.3)'
                ]
            }
        }
    },
    
    // Time axis
    timeAxis: {
        axisLine: {
            show: true,
            lineStyle: {
                color: '#333'
            }
        },
        axisTick: {
            show: true,
            lineStyle: {
                color: '#333'
            }
        },
        axisLabel: {
            show: true,
            color: '#333'
        },
        splitLine: {
            show: true,
            lineStyle: {
                color: [
                    '#ccc'
                ]
            }
        },
        splitArea: {
            show: false,
            areaStyle: {
                color: [
                    'rgba(250,250,250,0.3)',
                    'rgba(200,200,200,0.3)'
                ]
            }
        }
    },
    
    // Toolbox
    toolbox: {
        iconStyle: {
            borderColor: '#999'
        },
        emphasis: {
            iconStyle: {
                borderColor: '#666'
            }
        }
    },
    
    // Legend
    legend: {
        textStyle: {
            color: '#333'
        }
    },
    
    // Tooltip
    tooltip: {
        axisPointer: {
            lineStyle: {
                color: '#ccc',
                width: 1
            },
            crossStyle: {
                color: '#ccc',
                width: 1
            }
        }
    },
    
    // Timeline
    timeline: {
        lineStyle: {
            color: '#293c55',
            width: 1
        },
        itemStyle: {
            color: '#293c55',
            borderWidth: 1
        },
        controlStyle: {
            color: '#293c55',
            borderColor: '#293c55',
            borderWidth: 0.5
        },
        checkpointStyle: {
            color: '#e43c59',
            borderColor: '#c23531'
        },
        label: {
            color: '#293c55'
        },
        emphasis: {
            itemStyle: {
                color: '#a9334c'
            },
            controlStyle: {
                color: '#293c55',
                borderColor: '#293c55',
                borderWidth: 0.5
            },
            label: {
                color: '#293c55'
            }
        }
    },
    
    // Visual map
    visualMap: {
        color: [
            '#bf444c',
            '#d88273',
            '#f6efa6'
        ]
    },
    
    // Data zoom
    dataZoom: {
        backgroundColor: 'rgba(47,69,84,0)',
        dataBackgroundColor: 'rgba(47,69,84,0.3)',
        fillerColor: 'rgba(167,183,204,0.4)',
        handleColor: '#a7b7cc',
        handleSize: '100%',
        textStyle: {
            color: '#333'
        }
    },
    
    // Mark point
    markPoint: {
        label: {
            color: '#333'
        },
        emphasis: {
            label: {
                color: '#333'
            }
        }
    }
});
