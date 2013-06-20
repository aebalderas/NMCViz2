var field_series = [];
var model_series = [];
var routes = [];
var networkInfo =[];
load_data();

function load_data(){
    $.ajax({
        url : '/charts/loadvolume/' + db + '/' + host + '/' + pwd + '/' + user + '/' + links + '/' + start + '/' + end,
        dataType : 'json',
        cache : false,
        success : receive_data,
        error: function() {
	        alert("Unable to load data, See results.py, views.py, and urls.py")
        }
    });
}

function receive_data(json){
    for(var key in json.data){
        field_series.push(json.data[key]["count"]);
        model_series.push(json.data[key]["flow"]); 
        routes.push(json.data[key]["id"]);  
        networkInfo.push(json['networkName']);
    }
    makeColumnChart();
}

function makeColumnChart(){        
    $('#container').highcharts({
        chart: {
        type: 'column'
        },
        title: {
            text: 'Volume/Count Comparison'
        },
        subtitle: {
            text: networkInfo[0]
        },
        xAxis: {
            categories: routes              
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Vehicles'
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y:.1f}Vehicles</b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: [{
            name: 'Field Count',
            data: field_series
          },{
            name: 'Model Flow',
            data: model_series       
        }]
    });    
};    
