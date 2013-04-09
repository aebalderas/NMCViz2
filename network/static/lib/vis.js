var map;
var zoom = 14;
var eps4326; 
var dataLayer;
var linkmap = {};
var nodemap = {};
var busroutes = [];
var link_data = 0;
var node_data = 0;
var linkattrs = [];
var nodeattrs = [];
var current_time_step = 0;
var number_of_time_steps = 0;
var osm = 0;

$(document).ready(function() {

	map = new OpenLayers.Map("map");
	eps4326 = new OpenLayers.Projection("EPSG:4326");

	osm = new OpenLayers.Layer.OSM();
	osm.tileOptions.crossOriginKeyword = 'null';
	map.addLayers([osm]);
	
	linkattrs = [];
	
	for (var indx in links)
	{
		link = links[indx];
		lid = links[indx].linkid;
		linkmap[lid] = indx;
		
		for (var attr in link.attrs)
		{
			val = link.attrs[attr];
			if (typeof(linkattrs[attr]) == 'undefined') 
				linkattrs[attr] = [val, val]
			else
			{
				if (linkattrs[attr][0] > val)
					linkattrs[attr][0] = val;
				if (linkattrs[attr][1] < val)
					linkattrs[attr][1] = val;
			}
		}
	}
	
	nodeattrs = [];

	for (var indx in nodes)
	{
		node = nodes[indx];
		nodeid = nodes[indx].nodeid;
		point = nodes[indx].point;
		
		for (var attr in node.attrs)
		{
			val = node.attrs[attr];
			if (typeof(nodeattrs[attr]) == 'undefined') 
				nodeattrs[attr] = [val, val]
			else
			{
				if (nodeattrs[attr][0] > val)
					nodeattrs[attr][0] = val;
				if (nodeattrs[attr][1] < val)
					nodeattrs[attr][1] = val;
			}
		}
	}
	
	setup_link_data_options();
	setup_node_data_options();
	
	color_items(links, "#ff0000");
	color_items(nodes, "#00ff00");
	
	dataLayer = new OpenLayers.Layer.Vector("DataLayer", {
									eventListeners: {
										'featureselected': popup,
										'featureunselected': popdown
									}
								});
									
	map.addLayers([dataLayer]);
	
	var selectControl = new OpenLayers.Control.SelectFeature(dataLayer, {hover: true, autoActivate: true});
	map.addControl(selectControl);
	
	map.setCenter(new OpenLayers.LonLat(-97.7428, 30.2669).transform(eps4326, osm.projection), zoom);
	redraw();
});

function animate()
{
    if (current_time_step >= number_of_time_steps)
        current_time_step = 0;
        
    if (current_time_step < number_of_time_steps)
    {
      	current_time_step = current_time_step + 1;
      	link_color_selection();
      	node_color_selection();
      	redraw();
      	setTimeout(animate, 1000);
    }
}
   
var current_popup_feature = null;  

function popup(evt)
{
    if (current_popup_feature != null)
      popdown(current_popup_feature);
      
	feature = evt.feature;
	
	var s;
	
	if (feature.type == 'link')
    {
        link = feature.link;
        s = "link " + link.linkid;
        for (var a in link.attrs)
            s = s + '<br>    ' + a + ": " + link.attrs[a];
    }
    else
    {            
        node = feature.node;
        s = "node " + node.nodeid;
        for (var a in node.attrs)
            s = s + '<br>    ' + a + ": " + node.attrs[a];
    }       
            
	var popup = new OpenLayers.Popup.FramedCloud("popup", 
					OpenLayers.LonLat.fromString(feature.popup_location.toShortString()),
					null,
                    "<div style='font-size:.8em'>" + s + "</div>",
                    null,
                    true
                );
                
    feature.popup = popup;
    map.addPopup(popup);
    
    current_popup_feature = feature;
}

function popdown(evt)
{
	if (current_popup_feature != null)
	{
    	map.removePopup(current_popup_feature.popup);
    	current_popup_feature.popup.destroy();
    	current_popup_feature.popup = null;
   		current_popup_feature = null;
   	}
}

function setup_link_data_options()
{
	s = '<option value="constant">constant</option>';
	for (var a in linkattrs)
		s = s + '<option value="' + a + '">' + a + '</option>';
	if (link_data != 0)
		for (var a in link_data['minmax'])
			s = s + '<option value="' + a + '">' + a + '</option>';
		
	document.getElementById('link_color').innerHTML = s;
}

function setup_node_data_options()
{	
	s = '<option value="constant">constant</option>';
	for (var a in nodeattrs)
		s = s + '<option value="' + a + '">' + a + '</option>';
	if (node_data != 0)
		for (var a in node_data['minmax'])
			s = s + '<option value="' + a + '">' + a + '</option>';	
	document.getElementById('node_color').innerHTML = s;
}

function add_node_feature(node, color)
{
	node.geometry = new OpenLayers.Geometry.Point(node.point[0], node.point[1]).transform(eps4326, osm.projection);
	node.feature = new OpenLayers.Feature.Vector(node.geometry, null, {
													fillColor: '#66ffff', 
													fillOpacity: 0.2,
													strokeColor: '#66ffff',
													strokeOpacity: 1,
													strokeWidth: 1,
													pointRadius: '4'
												});

    node.feature.popup_location = node.geometry;
	node.feature.node = node;
	node.feature.type = 'node';
	
	return node;
}

function add_link_feature(link, offset)
{
	if (link.color != '')
	{
		var path;
		if (offset == 0)
			path = link.path;
		else
			path = offset_path(link.path, offset);
		
		pointArray = [];
		for (var p in path)
		{
			pt = path[p]
			g = new OpenLayers.Geometry.Point(pt[0], pt[1]).transform(eps4326, osm.projection);
			pointArray.push(g); 
		}
		
		link.linestring     = new OpenLayers.Geometry.LineString(pointArray);
		link.feature        = new OpenLayers.Feature.Vector(link.linestring, null, {
													strokeColor: link.color,
													strokeOpacity: 1,
													strokeWidth: 2});
													
		p0 = path[ 0];
		p1 = path[path.length-1];
		p = [(p0[0] + p1[0]) / 2.0, (p0[1] + p1[1]) / 2.0];
		link.feature.popup_location = new OpenLayers.Geometry.Point(p[0], p[1]).transform(eps4326, osm.projection);
		
		link.feature.link 			=  link;
		link.feature.type 			= 'link';
		return true;
	}
	else
		return false;
}


function color_items_by_fixed_attribute(list, minmax, attr)
{
	vmin = minmax[attr][0];
	vmax = minmax[attr][1];
	
	for (var i in list)
	{
		item = list[i]
		if (typeof(item.attrs[attr]) == 'undefined')
			item.color = '';
		else
		{
			val = item.attrs[attr];
			item.color = val_to_color(val, vmin, vmax);
		}
	}
}

function color_items_by_varying_attribute(list, map, data, minmax, attr, timestep)
{
	vmin = minmax[attr][0];
	vmax = minmax[attr][1];
	
	for (var i in list)
	{
		item = links[i];
		item.color = '';
	}

	timestep_data = data[timestep];
	ids  = timestep_data['linkids'];
	vals = timestep_data[attr];

	for (var i = 0, j = ids.length; i < j; i++)
	{
		id = ids[i];
		val = vals[i];
		list[map[id]].color = val_to_color(val, vmin, vmax);
	}
}

function color_items(list, color)
{
	for (var i in list)
	{
		item = list[i];
		item.color = color;
	}
}
	
function link_color_selection()
{
	attr = document.getElementById('link_color').value;
	
	if (typeof(linkattrs[attr]) != 'undefined') 
	{
		color_items_by_fixed_attribute(links, linkattrs, attr);
	}
	else if (link_data != 0 && typeof(link_data['minmax'][attr]) != 'undefined')
	{
	    color_items_by_varying_attribute(links, linkmap, link_data['data'], link_data['minmax'], attr, current_time_step)
	}
	else
	    color_items("#ff0000");

    conditionally_setup_animation();
	redraw();
}

function conditionally_setup_animation()
{
	document.getElementById('animate').disabled = true;
    
    if (node_data != 0)
    {
        attr = document.getElementById('node_color').value;
        if (typeof(node_data['minmax'][attr]) != 'undefined')
			document.getElementById('animate').disabled = false;
	}
	
	if (link_data != 0)
	{
		attr = document.getElementById('link_color').value;
		if (typeof(link_data['minmax'][attr]) != 'undefined')
			document.getElementById('animate').disabled = false;
	}
}

function  node_color_selection()
{	
	attr = document.getElementById('node_color').value;
	
	if (typeof(node.attrs[attr]) != 'undefined') 
	{
		color_items_by_fixed_attribute(nodes, node.attrs[attr], attr);
	}
	else if (node_data != 0 && typeof(node_data['minmax'][attr]) != 'undefined')
	{
	    current_time_step = 0;
	    number_of_time_steps = node_data['data'].length;
	    color_items_by_varying_attribute(nodes, nodemap, node_data['data'], node_data['minmax'][attr], attr, current_timestep)
	    document.getElementById('load_data').disabled = false
	    
	}
	else
	    color_items("#ff0000");

    conditionally_setup_animation();
	redraw();
}

function redraw()
{
	offset = parseFloat(document.getElementById("link_offset").value);
	
	linkCheckBoxes = document.getElementsByName('linktypes');
	checkedLinkTypes = {}
	for (var i = 0, j = linkCheckBoxes.length; i < j; i++)
		if (linkCheckBoxes[i].checked)
			checkedLinkTypes[linkCheckBoxes[i].value] = 1
	
	nodeCheckBoxes = document.getElementsByName('nodetypes')
	checkedNodeTypes = {}
	for (var i = 0, j = nodeCheckBoxes.length; i < j; i++)
		if (nodeCheckBoxes[i].checked)
			checkedNodeTypes[nodeCheckBoxes[i].value] = 1
	
	busRouteCheckBoxes = document.getElementsByName('busroutes')
	checkedBusRoutes = {}
	for (var i = 0, j = busRouteCheckBoxes.length; i < j; i++)
		if (busRouteCheckBoxes[i].checked)
			checkedBusRoutes[busRouteCheckBoxes[i].value] = 1

	dataLayer.removeAllFeatures();
	
	features = []
	
	for (var indx in nodes)
	{
		if (nodes[indx].type in checkedNodeTypes)
		{
			nnode = add_node_feature(nodes[indx], "");
			nodes[indx] = nnode;
			features.push(nodes[indx].feature);
		}
	}	  
	
	if (document.getElementById("selection_type_nodelink").checked)
		for (var indx in links)
		{
			link = links[indx];
			
			if (link.type in checkedLinkTypes)
			{
				if (add_link_feature(link, offset))
				features.push(links[indx].feature);
			}
		}
		else
		{
			busRouteCheckBoxes = document.getElementsByName('busroutes');
			for (var i = 0, j = busRouteCheckBoxes.length; i < j; i = i + 1)
			{
				if (busRouteCheckBoxes[i].checked)
				{
					route = busroutes[busRouteCheckBoxes[i].value];
					for (var l in route)
					{
						link = links[linkmap[route[l]]];
						if (add_link_feature(link, offset))
							features.push(link.feature);
					}
				}
			}
		}

	dataLayer.addFeatures(features);
	dataLayer.redraw();        
}

function receive_data(data)
{
	if (data['status'] != 'OK')
		alert('Data access error: ' + data['status']);
	else
	{
		link_data = data;
	
		minmax = {}
		for (var a in link_data['attributes'])
		{
			attr = link_data['attributes'][a];
			minmax[attr] = 0
		}
		
		for (var t in link_data['data'])
		{
			tstep = link_data['data'][t];
			for (var a in link_data['attributes'])
			{
				attr = link_data['attributes'][a];
				arr = tstep[attr];
				m = Math.min.apply(Math, arr);
				M = Math.max.apply(Math, arr);
				
				if (minmax[attr] == 0)
					minmax[attr] = [Math.min.apply(Math, arr), Math.max.apply(Math, arr)];
				else
				{
					if (m < minmax[attr][0]) minmax[attr][0] = m;
					if (M > minmax[attr][1]) minmax[attr][1] = M;
				}
			}
		}
		
		link_data['minmax'] = minmax;
	
		setup_link_data_options();
		setup_node_data_options();
		
		current_time_step = 0;
		number_of_time_steps = link_data['data'].length;
		
		link_color_selection();
		node_color_selection();
	}
}
	
function load_data()
{
	$.ajax({
		url: '/network/load_data/' + network_name + 
				'/' + document.getElementById('data_start').value + 
				'/' + document.getElementById('data_interval').value + 
				'/' + document.getElementById('data_end').value,
		dataType : 'json',
		cache: false,
		success: receive_data
		});
}

function check_load_data()
{
	if ((document.getElementById('data_start').value != "") &&
		(document.getElementById('data_interval').value != "") &&
		(document.getElementById('data_end').value != ""))
			document.getElementById('load_data').disabled = false
}

function selection_type()
{
	v = document.getElementById('selection_type_nodelink').checked
	
	if (v)
	{
		document.getElementById('busRouteSelect').style.visibility = "hidden";
		document.getElementById('nodeLinkTypeSelect').style.visibility = "visible";
	}
	else
	{
		document.getElementById('nodeLinkTypeSelect').style.visibility = "hidden";
		document.getElementById('busRouteSelect').style.visibility = "visible";
	}
	redraw();
}

function Interpolate(start, end, steps, count) 
{
	var s = start;
	var e = end;
	var final = s + (((e - s) / steps) * count);
	return Math.floor(final);
}

function val_to_color(v, min, max)
{
	val = 100.0 * (v - min)/(max - min);
	
	if (val > 50)
	{
		start = [0,255,0];
		end   = [255,0,0];
		val   = val - 50.0;
	}
	else
	{
		start = [0,0,255];
		end   = [0,255,0];
	}
	
	var r = Interpolate(start[0], end[0], 50, val);
	var g = Interpolate(start[1], end[1], 50, val);
	var b = Interpolate(start[2], end[2], 50, val);
	
	if (r < 16) rs = '0' + r.toString(16);
	else rs = r.toString(16);
	
	if (g < 16) gs = '0' + g.toString(16);
	else gs = g.toString(16);
	
	if (b < 16) bs = '0' + b.toString(16);
	else bs = b.toString(16);
	
	return "#" + rs + gs + bs;
}

function val_to_width(v, min, max)
{
    val = Math.floor((v / max) * 10);
    return val    
}

function toggleMap(onOff)
{
	if (osm.getVisibility())
		osm.setVisibility(false);
	else
		osm.setVisibility(true);
}

