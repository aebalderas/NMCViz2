var linklist = []; //categories
var right = [];
var left = [];
var through = [];
var networkInfo = [];

function makeGraph() {
    $('#container').highcharts({
        chart: {
            type: 'bar'
        },
        title: {
            text: 'Turning Movements'
        },
        xAxis: {
            categories: linklist
        },
        yAxis: {
            min: 0,
            title: {
                text: networkInfo[0]
            }
        },
        legend: {
            backgroundColor: '#FFFFFF',
            reversed: true
        },
        plotOptions: {
            series: {
                stacking: 'normal'
            }
        },
        series: [{
            name: 'Right',
            data: right
        }, {
            name: 'Left',
            data: left
        }, {
            name: 'Through',
            data: through
        }]
    });
}
 
function receive_data(json) {

    networkInfo.push(json["network"]);
    for(var key in json["link"]) {
        linklist.push(json["link"][key]);
    }
    for(var key in json["data"]) {
        if(json["data"][key]["direction"] == 'left'){
            left.push(json["data"][key]["count"]);
            right.push[0];
            through.push[0];
        }else if(json["data"][key]["direction"] == "right"){
            right.push(json["data"][key]["count"]);
            left.push[0];
            through.push[0];
        }else{
            through.push(json["data"][key]["count"]);
            left.push[0];
            right.push[0];
        }
    }
	makeGraph();
}
function load_data() {
    $.ajax({
        url: '/charts/loadturnmove/' + db + '/' + host + '/' + pwd + '/' + user + '/' + links,
        dataType: 'json',
        cache: false,
        success: receive_data,
        error: function() {
            alert("unable to load data");
        }
    });
}

    
load_data();
    
