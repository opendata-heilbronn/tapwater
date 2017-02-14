var chart = {
    hardness: [],
    date: [],
    sodium: [],
    calcium: [],
    potassium: [],
    sulfate: [],
    chloride: [],
    nitrate: [],
    magnesium: []
};

/**
 * Add value to sodium array
 * @param value
 */
chart.addSodium = function (value) {
    if ((value.split("-")).length > 1) {
        var stSplit = value.split("-");
        chart.sodium.push((parseInt(stSplit[0]) + parseInt(stSplit[1]))/2);
    } else {
        if (value == ""){
            chart.sodium.push(null);
        } else {
            chart.sodium.push(value);
        }
    }
};

/**
 * Add value to hardness array
 * @param value
 */
chart.addHardness = function (value) {
    if ((value.split("-")).length > 1) {
        var stSplit = value.split("-");
        chart.hardness.push((parseInt(stSplit[0]) + parseInt(stSplit[1]))/2);
    } else {
        if (value == ""){
            chart.hardness.push(null);
        } else {
            chart.hardness.push(value);
        }
    }
};

/**
 * Add value to calcium array
 * @param value
 */
chart.addCalcium = function (value) {
    if ((value.split("-")).length > 1) {
        var stSplit = value.split("-");
        chart.calcium.push((parseInt(stSplit[0]) + parseInt(stSplit[1]))/2);
    } else {
        if (value == ""){
            chart.calcium.push(null);
        } else {
            chart.calcium.push(value);
        }
    }
};

/**
 * Add value to sulfate array
 * @param value
 */
chart.addSulfate = function (value) {
    if ((value.split("-")).length > 1) {
        var stSplit = value.split("-");
        chart.sulfate.push((parseInt(stSplit[0]) + parseInt(stSplit[1]))/2);
    } else {
        if (value == ""){
            chart.sulfate.push(null);
        } else {
            chart.sulfate.push(value);
        }
    }
};

/**
 * Add value to potassium array
 * @param value
 */
chart.addPotassium = function (value) {
    if ((value.split("-")).length > 1) {
        var stSplit = value.split("-");
        chart.potassium.push((parseInt(stSplit[0]) + parseInt(stSplit[1]))/2);
    } else {
        if (value == ""){
            chart.potassium.push(null);
        } else {
            chart.potassium.push(value);
        }
    }
};

/**
 * Add value to chloride array
 * @param value
 */
chart.addChloride = function (value) {
    if ((value.split("-")).length > 1) {
        var stSplit = value.split("-");
        chart.chloride.push((parseInt(stSplit[0]) + parseInt(stSplit[1]))/2);
    } else {
        if (value == ""){
            chart.chloride.push(null);
        } else {
            chart.chloride.push(value);
        }
    }
};

/**
 * Add value to nitrate array
 * @param value
 */
chart.addNitrate = function (value) {
    if ((value.split("-")).length > 1) {
        var stSplit = value.split("-");
        chart.nitrate.push((parseInt(stSplit[0]) + parseInt(stSplit[1]))/2);
    } else {
        if (value == ""){
            chart.nitrate.push(null);
        } else {
            chart.nitrate.push(value);
        }
    }
};

/**
 * Add value to magnesium array
 * @param value
 */
chart.addMagnesium = function (value) {
    if ((value.split("-")).length > 1) {
        var stSplit = value.split("-");
        chart.magnesium.push((parseInt(stSplit[0]) + parseInt(stSplit[1]))/2);
    } else {
        if (value == ""){
            chart.magnesium.push(null);
        } else {
            chart.magnesium.push(value);
        }
    }
};

/**
 * Add value to date array
 * @param value
 */
chart.addDate = function (value) {
    chart.date.push(value);
};

/**
 * Create charts.
 */
chart.createCharts = function(xaxis, yaxis) {

    var data_sodium = {
        labels: chart.date,
        series: [ chart.sodium ]
    };

    var data_hardness = {
        labels: chart.date,
        series: [ chart.hardness ]
    };

    var data_calcium = {
        labels: chart.date,
        series: [ chart.calcium ]
    };

    var data_potassium = {
        labels: chart.date,
        series: [ chart.potassium ]
    };

    var data_sulfate = {
        labels: chart.date,
        series: [ chart.sulfate ]
    };

    var data_nitrate = {
        labels: chart.date,
        series: [ chart.nitrate ]
    };

    var data_chloride = {
        labels: chart.date,
        series: [ chart.chloride ]
    };

    var data_magnesium = {
        labels: chart.date,
    series: [ chart.magnesium ]
    };


    var options_sodium = {
        high: 200,
        low: 0,
        plugins: [
        Chartist.plugins.tooltip({
          currency: 'mg/l ',
          appendToBody: true
        }
        ),
        Chartist.plugins.ctAxisTitle({
          axisX: {
            axisTitle: xaxis,
            axisClass: 'ct-axis-title',
            offset: {
              x: 0,
              y: 30
            },
            textAnchor: 'middle'
          },
          axisY: {
            axisTitle: yaxis  + ' (mg/l)',
            axisClass: 'ct-axis-title',
            offset: {
              x: 0,
              y: -1
            },
            textAnchor: 'middle',
            flipTitle: false
          }
        })
      ]
     };

    var options_hardness = {
        high: 45,
        low: 0,
        plugins: [
        Chartist.plugins.tooltip({
          currency: '°dH ',
          appendToBody: true
        }
        ),
        Chartist.plugins.ctAxisTitle({
          axisX: {
            axisTitle: xaxis,
            axisClass: 'ct-axis-title',
            offset: {
              x: 0,
              y: 30
            },
            textAnchor: 'middle'
          },
          axisY: {
            axisTitle: yaxis  + ' (°dH)',
            axisClass: 'ct-axis-title',
            offset: {
              x: 0,
              y: -1
            },
            textAnchor: 'middle',
            flipTitle: false
          }
        })
      ]
     };

    var options_sulfate = {
        high: 250,
        low: 0,
        plugins: [
        Chartist.plugins.tooltip({
          currency: 'mg/l ',
          appendToBody: true
        }
        ),
        Chartist.plugins.ctAxisTitle({
          axisX: {
            axisTitle: xaxis,
            axisClass: 'ct-axis-title',
            offset: {
              x: 0,
              y: 30
            },
            textAnchor: 'middle'
          },
          axisY: {
            axisTitle: yaxis + ' (mg/l)',
            axisClass: 'ct-axis-title',
            offset: {
              x: 0,
              y: -1
            },
            textAnchor: 'middle',
            flipTitle: false
          }
        })
      ]
    };

    var options_nitrate = {
        high: 65,
        low: 0,
        plugins: [
        Chartist.plugins.tooltip({
          currency: 'mg/l ',
          appendToBody: true
        }
        ),
        Chartist.plugins.ctAxisTitle({
          axisX: {
            axisTitle: xaxis,
            axisClass: 'ct-axis-title',
            offset: {
              x: 0,
              y: 30
            },
            textAnchor: 'middle'
          },
          axisY: {
            axisTitle: yaxis + ' (mg/l)',
            axisClass: 'ct-axis-title',
            offset: {
              x: 0,
              y: -2
            },
            textAnchor: 'middle',
            flipTitle: false
          }
        })
      ]
    };

    var options_chloride = {
        high: 260,
        low: 0,
        plugins: [
        Chartist.plugins.tooltip({
          currency: 'mg/l ',
          appendToBody: true
        }
        ),
        Chartist.plugins.ctAxisTitle({
          axisX: {
            axisTitle: xaxis,
            axisClass: 'ct-axis-title',
            offset: {
              x: 0,
              y: 30
            },
            textAnchor: 'middle'
          },
          axisY: {
            axisTitle: yaxis + ' (mg/l)',
            axisClass: 'ct-axis-title',
            offset: {
              x: 0,
              y: -2
            },
            textAnchor: 'middle',
            flipTitle: false
          }
        })
      ]
    };

    var options_magnesium = {
        high: 65,
        low: 0,
        plugins: [
        Chartist.plugins.tooltip({
          currency: 'mg/l ',
          appendToBody: true
        }
        ),
        Chartist.plugins.ctAxisTitle({
          axisX: {
            axisTitle: xaxis,
            axisClass: 'ct-axis-title',
            offset: {
              x: 0,
              y: 30
            },
            textAnchor: 'middle'
          },
          axisY: {
            axisTitle: yaxis + ' (mg/l)',
            axisClass: 'ct-axis-title',
            offset: {
              x: 0,
              y: -2
            },
            textAnchor: 'middle',
            flipTitle: false
          }
        })
      ]
    };

    var options_calcium = {
        high: 450,
        low: 0,
        plugins: [
        Chartist.plugins.tooltip({
          currency: 'mg/l ',
          appendToBody: true
        }
        ),
        Chartist.plugins.ctAxisTitle({
          axisX: {
            axisTitle: xaxis,
            axisClass: 'ct-axis-title',
            offset: {
              x: 0,
              y: 30
            },
            textAnchor: 'middle'
          },
          axisY: {
            axisTitle: yaxis + ' (mg/l)',
            axisClass: 'ct-axis-title',
            offset: {
              x: 0,
              y: -2
            },
            textAnchor: 'middle',
            flipTitle: false
          }
        })
      ]
    };

    var options_potassium = {
        high: 15,
        low: 0,
        plugins: [
        Chartist.plugins.tooltip({
          currency: 'mg/l ',
          appendToBody: true
        }
        ),
        Chartist.plugins.ctAxisTitle({
          axisX: {
            axisTitle: xaxis,
            axisClass: 'ct-axis-title',
            offset: {
              x: 0,
              y: 30
            },
            textAnchor: 'middle'
          },
          axisY: {
            axisTitle: yaxis + ' (mg/l)',
            axisClass: 'ct-axis-title',
            offset: {
              x: 0,
              y: -2
            },
            textAnchor: 'middle',
            flipTitle: false
          }
        })
      ]
    };

    var options_responsive = [
      ["screen and (max-width: 640px)", {
        showLine: true,
        showArea: false
      }]
    ];

    // Create a new line chart object where as first parameter we pass in a selector
    // that is resolving to our chart container element. The Second parameter
    // is the actual data object.
    if(data_sodium.labels.length > 0){
        new Chartist.Line('#sodium_chart', data_sodium, options_sodium, options_responsive);
    }
    if(data_hardness.labels.length > 0){
        new Chartist.Line('#hardness_chart', data_hardness, options_hardness, options_responsive);
    }
    if(data_calcium.labels.length > 0){
        new Chartist.Line('#calcium_chart', data_calcium, options_calcium, options_responsive);
    }
    if(data_potassium.labels.length > 0){
        new Chartist.Line('#potassium_chart', data_potassium, options_potassium, options_responsive);
    }
    if(data_sulfate.labels.length > 0){
        new Chartist.Line('#sulfate_chart', data_sulfate, options_sulfate, options_responsive);
    }
    if(data_nitrate.labels.length > 0){
        new Chartist.Line('#nitrate_chart', data_nitrate, options_nitrate, options_responsive);
    }
    if(data_chloride.labels.length > 0){
        new Chartist.Line('#chloride_chart', data_chloride, options_chloride, options_responsive);
    }
    if(data_magnesium.labels.length > 0){
        new Chartist.Line('#magnesium_chart', data_magnesium, options_magnesium, options_responsive);
    }
 };


