host:var osm_map;
var zoom					= 12;
var eps4326; 
var dataLayer;
var linkmap 				= {};
var nodemap 				= {};
var busroutes 				= [];
var link_data				= 0;
var node_data 				= 0;
var link_offset_WCS 		= 0.0001;
var current_timestep 		= 0;
var number_of_timesteps 	= 0;
var osm 					= 0;
var node_attributes			= [];
var node_features   		= [];
var	link_attributes			= [];
var link_features   		= []
var offset_link_features 	= [];
var path_datasets       	= [];
var path_origins			= [];
var path_destinations		= [];
var path_link_attributes    = [];
var path_link_timesteps		= [];
var popups_on       		= true;
var animation_delay 		= 1;
var animation_running 		= false;
var path_destination_node 	= -1;
var path_origin_node      	= -1;
var path_properties 		= [];
var map_intensity 			= 1.0
var controlsHidden = false;
var popupControl;
var selectionControl;

$(document).ready(function() {

	load_network(network_name);
	
	osm_map = new OpenLayers.Map("map");
	eps4326 = new OpenLayers.Projection("EPSG:4326");

	osm = new OpenLayers.Layer.OSM();
	osm.tileOptions.crossOriginKeyword = 'null';
	osm_map.addLayers([osm]);
	change_map_intensity(1.0)
    
	dataLayer = new OpenLayers.Layer.Vector("DataLayer");									
	osm_map.addLayers([dataLayer]);
	
	popupControl = new OpenLayers.Control.SelectFeature(dataLayer)
	selectionControl = new OpenLayers.Control.SelectFeature(dataLayer, {box: true, multiple: true, clickout: true});
	
	dataLayer.events.on({'featureselected': popup, 'featureunselected': popdown})
	osm_map.addControl(popupControl);
    popupControl.activate();
	
	$( "#dialog" ).dialog({autoOpen: false});
});

// toggle the control section of html
function toggleControls() {
    if (controlsHidden == false) { // not hidden --> hide
		$('#controls').animate({"left": "-=15%", "width": "-=15%"},
							    "slow"); 
		$('#map').animate({"width": "+=14%"}, "slow"); 
		controlsHidden = true;
	}
	else {
		$('#map').animate({"width": "-=14%"}, "slow");
		$('#controls').animate({"left": "+=15%", "width": "+=15%"}, "slow");
		controlsHidden = false;
	}
}

function position_map(lon, lat, d)
{
	zoom = 14 - 4*(d - 0.1) / (2.81 - 0.1)
	osm_map.setCenter(new OpenLayers.LonLat(lon, lat).transform(eps4326, osm.projection), zoom); 
}
 
var selectedNodeList = []
var target_text = ''

function nodeSelected(ev)
{
	selectedNodeList.push(ev.feature.feature_id)
	document.getElementById(target_text).value = selectedNodeList.join()
}

function selectNodes()
{	
	document.getElementById('origin_selection_done_button').style.visibility = "visible"
	document.getElementById('origin_selection_clear_button').style.visibility = "visible"
	document.getElementById('destination_selection_done_button').style.visibility = "hidden"
	document.getElementById('destination_selection_clear_button').style.visibility = "hidden"
	document.getElementById('new_path_selection_button').style.visibility = "hidden"

	document.getElementById('path_origins').value = ''
	document.getElementById('path_destinations').value = ''
		
	path_origins			= []
	path_destinations		= []
	path_link_attributes    = []
	path_link_timesteps		= []
	
	load_path_origins()
	
	popdown()
	popupControl.unselectAll()
	popupControl.deactivate()
	osm_map.removeControl(popupControl)
	
	target_text = 'path_origins'
	selectedNodeList = []
	
	dataLayer.events.on({'featureselected': nodeSelected})
	dataLayer.events.remove('featureunselected')
	
	osm_map.addControl(selectionControl)
	selectionControl.activate()
}

function origin_selection_clear()
{
	selectedNodeList = []
	document.getElementById('path_origins').value = ""
}

function destination_selection_clear()
{
	selectedNodeList = []
	document.getElementById('path_destinations').value = ""
}

function origin_selection_done()
{
	load_path_destinations()
	
	target_text = 'path_destinations'
	selectedNodeList = []
	
	document.getElementById('origin_selection_done_button').style.visibility = "hidden"
	document.getElementById('origin_selection_clear_button').style.visibility = "hidden"
	
	document.getElementById('destination_selection_clear_button').style.visibility = "visible"
	document.getElementById('destination_selection_done_button').style.visibility = "visible"
}

function destination_selection_done()
{	
	load_paths()
	
	document.getElementById('destination_selection_done_button').style.visibility = "hidden"
	document.getElementById('new_path_selection_button').style.visibility = "visible"
	
	selectNodesDone()
}

function new_path_selection()
{
	selectNodes()
}

function selectNodesDone()
{
	selectionControl.unselectAll()
	selectionControl.deactivate()
	osm_map.removeControl(selectionControl)
	
	dataLayer.events.on({'featureselected': popup, 'featureunselected': popdown})
	osm_map.addControl(popupControl)
	popupControl.activate()
}
	
function resize_map()
{
    main_container = document.getElementById('main_container')
    main_container_height = main_container.offsetHeight
    
    map = document.getElementById('map')
    map_offset = map.offsetTop
    
    new_height = main_container_height - map_offset
    
    map.style.height = new_height + "px"
    osm_map.updateSize()
}
  
function attribute_minmax(attr)
{
	m =  Number.MAX_VALUE
    M = -Number.MAX_VALUE
    
    for (var i in attr.data)
    {
        mm = Math.min.apply(null, attr.data[i])
        MM = Math.max.apply(null, attr.data[i])
        if (m > mm) m = mm
        if (M < MM) M = MM
    }
    
    attr['range'] = [m,M]
}

function post_node_types(types)
{
	str = ''
	for (var i in types)
	  str += '<input type="checkbox" name="nodetypes" value=' + types[i] + ' onclick="redraw()">' + types[i] + '<br>'
	
	document.getElementById('nodeTypes').innerHTML = str;
}

function post_link_types(types)
{
	str = ''
	for (var i in types)
		if (types[i] == 1)
	  		str += '<input type="checkbox" name="linktypes" value=' + types[i] + ' onclick="redraw()" checked>' + types[i] + '<br>'
	  	else
	  		str += '<input type="checkbox" name="linktypes" value=' + types[i] + ' onclick="redraw()">' + types[i] + '<br>'
	
	document.getElementById('linkTypes').innerHTML = str;
}

function post_busroutes(routes)
{
	str = ''
	for (var rte in routes)
	{
	    str += '<div style="width:45px;height:20px;float:left;position:relative">'
	    str += '  <input type="checkbox" name="busroutes" value="' + rte + '" checked="yes" onclick=redraw() >' + rte
	    str += '</div>'
	}
	
	document.getElementById('busroutes').innerHTML = str;
}

function receive_network(data)
{
	nodemap 		= {}
	
	min_lat =  999
	max_lat = -999
	min_lon =  999
	max_lon = -999
	
	for (var n in data.nodes)
	{
		node = data.nodes[n]
		node_features.push(create_node_feature(node[0], node[1], node[2]))
		if (node[2][0] < min_lon) min_lon = node[2][0]
		if (node[2][0] > max_lon) max_lon = node[2][0]
		if (node[2][1] < min_lat) min_lat = node[2][1]
		if (node[2][1] > max_lat) max_lat = node[2][1]
		nodemap[node[0]] = n;
	}

	dlon = max_lon - min_lon
	dlat = max_lat - min_lat
	d = Math.sqrt(dlon*dlon + dlat*dlat)
	
    position_map((max_lon + min_lon) / 2.0, (max_lat + min_lat) / 2.0, d)
    
	post_node_types(data.nodeTypes)
	
	for (var varname in data.nodeAttributes)
	{
		attribute = data.nodeAttributes[varname]
		attribute_minmax(attribute)
		node_attributes[varname] = attribute
	}
	
	post_node_color_options("constant")
	 
	linkmap         = {}
	
	for (var l in data.links)
	{
		link = data.links[l]
		
		link_features.push(create_link_feature(link[0], link[1], link[4], false))
		offset_link_features.push(create_link_feature(link[0], link[1], link[4], true))
		
		linkmap[link[0]] = l;
	}
	        	
	post_link_types(data.linkTypes)

	for (var varname in data.linkAttributes)
	{
		attribute = data.linkAttributes[varname]
		attribute_minmax(attribute)
		link_attributes[varname] = attribute
	}
	
	busroutes = data.busroutes
	post_busroutes(busroutes)
	
	post_link_color_options("constant")		
	post_path_data_options("")
	
	color_links()
	color_nodes()
	
	redraw();
}
	
function load_network()
{
	$.ajax({
		url: '/network/load_network/' + network_name,
		dataType : 'json',
		cache: false,
		success: receive_network
		});
}

function stop_animation()
{
	stop_flag = true;
}

function animation_toggle()
{
	if (animation_running == true)
	{
	    animation_running = false
	    document.getElementById('run_animation_button').value = 'Run '
	}
	else
	{
		set_current_timestep(0)
		animation_running = true
		document.getElementById('run_animation_button').value = 'Stop'
		animate()
	}
}

function animation_step()
{
	if (get_current_timestep() >= number_of_timesteps-1)
	  set_current_timestep = -1
	  
	set_current_timestep(get_current_timestep() + 1)
	
	color_links()
	color_nodes()
	redraw()
}

function increment_current_timestep()
{
	set_current_timestep(current_timestep+1)
}

function set_current_timestep(n)
{
	current_timestep = n
    document.getElementById('current_timestep').innerHTML = n
}

function get_current_timestep()
{
	return current_timestep;
}


function animate()
{
	if (animation_running)
	{
		if (get_current_timestep() >= (number_of_timesteps-1))
		{
			animation_toggle()
		}
		else
		{
			color_links()
			color_nodes()
			redraw()
			increment_current_timestep()
			setTimeout(animate, animation_delay);
		}
	}
}
   
var current_popup_feature = null;  

function show_popups(v)
{
	popups_on = v;
}

function popup(evt)
{
    if (current_popup_feature != null)
	    popdown(evt)

	if (popups_on)
	{
		feature = evt.feature;
		
		var s;
		
		if (feature.type == 'link')
	    {
	        link = feature.feature_id
	        s = "link " + link
	        indx = linkmap[link]
	        for (var a in link_attributes)
	        {
	        	data = link_attributes[a].data
	        	if (data.length == 1)
	        		v = link_attributes[a].data[0][indx]
	        	else
	        		v = link_attributes[a].data[get_current_timestep()][indx]
	            s = s + '<br>    ' + a + ": " + v;
	        }
	    }
	    else
	    {            
	        node = feature.feature_id;
			s = "node " + node + '<br>Lat: ' + feature.location[1] + ' Lon: ' + feature.location[0]
	        indx = nodemap[node]
	        for (var a in node_attributes)
	            s = s + '<br>    ' + a + ": " + node_attributes[a].data[get_current_timestep()][indx];
	    }       
	            
		var popup = new OpenLayers.Popup.FramedCloud("popup", 
						OpenLayers.LonLat.fromString(feature.popup_location.toShortString()),
						null,
	                    "<div style='font-size:.8em'>" + s + "</div>",
	                    null,
	                    true
	                );
	                
	    feature.popup = popup;
	    osm_map.addPopup(popup);
	    
	    current_popup_feature = feature;
	}
}

function popdown(evt)
{
	if (current_popup_feature != null)
	{
    	osm_map.removePopup(current_popup_feature.popup);
    	current_popup_feature.popup.destroy();
    	current_popup_feature.popup = null;
   		current_popup_feature = null;
   	}
}

function post_link_color_options(which)
{
	if (which == "" || which == "constant")
		s = '<option value="constant" selected>constant</option>';
	else
		s = '<option value="constant">constant</option>';
	
	for (var a in link_attributes)
	    if (a == which)
			s = s + '<option value="' + a + '" selected>' + a + '</option>';
		else
			s = s + '<option value="' + a + '">' + a + '</option>';
		
	document.getElementById('link_color_select').innerHTML = s;
}

function post_path_data_options(which)
{
	var html_string;
    if (path_data_select.length == 0)
		html_string = '<option value="none" selected>(none)</option>';
    else
    {
    	html_string = ""
    	for (var a in path_datasets)
    	{
    	    d = path_datasets[a]
		    if (which != "" && d == which)
				html_string = html_string + '<option value="' + d + '" selected>' + d + '</option>';
			else
				html_string = html_string + '<option value="' + d + '">' + d + '</option>';
		}
    }

	document.getElementById('path_data_select').innerHTML = html_string;
}
function post_node_color_options(which)
{	
	if (which == "" || which == "constant")
		s = '<option value="constant" selected>constant</option>';
	else
		s = '<option value="constant">constant</option>';
	
	for (var a in node_attributes)
	    if (which == a)
			s = s + '<option value="' + a + '" selected>' + a + '</option>';
		else
			s = s + '<option value="' + a + '">' + a + '</option>';

	document.getElementById('node_color_select').innerHTML = s;
}

function post_path_color_options(which)
{	
if (which == "" || which == "constant")
		s = '<option value="constant" selected>constant</option>';
	else
		s = '<option value="constant">constant</option>';
		
		
	for (var a in path_link_attributes)
	    if (which == a)
			s = s + '<option value="' + a + '" selected>' + a + '</option>';
		else
			s = s + '<option value="' + a + '">' + a + '</option>';

	document.getElementById('path_color_select').innerHTML = s;
}

function create_node_feature(id, type, location)
{
	geometry = new OpenLayers.Geometry.Point(location[0], location[1]).transform(eps4326, osm.projection);
	feature = new OpenLayers.Feature.Vector(geometry, null, {
													fillColor: "#ff0000", 
													fillOpacity: 0.2,
													strokeColor: "#ff0000",
													strokeOpacity: 1,
													strokeWidth: 1,
													pointRadius: '4'
												});

	feature.location		= location;
    feature.popup_location 	= geometry;
	feature.feature_id		= id;
	feature.type 			= 'node';
	feature.nodeType 		= type;
	return feature;
}

function create_link_feature(id, type, path, offset)
{
	var feature_path;
	
	if (offset)
		feature_path = offset_path(path, link_offset_WCS);
	else
		feature_path = path;
	
	pointArray = [];
	for (var p in feature_path)
	{
		try
		{
			pt = feature_path[p]
			g = new OpenLayers.Geometry.Point(pt[0], pt[1]).transform(eps4326, osm.projection);
			pointArray.push(g); 
		} catch(e) {
			console.log('create_link_feature')
		}
	}
	
	linestring     = new OpenLayers.Geometry.LineString(pointArray);
	feature        = new OpenLayers.Feature.Vector(linestring, null, {
												strokeColor: "#ff0000",
												strokeOpacity: 1,
												strokeWidth: 2});
												
	p0 = path[ 0];
	p1 = path[path.length-1];
	p = [(p0[0] + p1[0]) / 2.0, (p0[1] + p1[1]) / 2.0];
	
	feature.popup_location = new OpenLayers.Geometry.Point(p[0], p[1]).transform(eps4326, osm.projection);
	
	feature.feature_id 		=  id;
	feature.type 			= 'link';
	feature.linkType 		= type;
	feature.isOffset		= offset;
	
	return feature;
}

function color_feature(feature, color)
{
	if (feature != undefined)
	{
		feature.style['strokeColor'] = color;
		feature.style['fillColor'] = color;
	}
}

function color_features(features, color)
{
	for (var i in features)
		color_feature(features[i], color);
}

function color_features_by_attribute(features, map, attribute, timestep)
{
	vmin = attribute['range'][0]
	vmax = attribute['range'][1]
	
	color_features(features, '')
	  
	timestep_data = attribute.data[timestep]
	for (var i in attribute.ids)
	{
	  	indx = map[attribute.ids[i]]
		color_feature(features[indx], val_to_color(timestep_data[i], vmin, vmax));
	}
}

function color_paths_by_path_attribute(how, timestep)
{
	vmax = path_link_attributes[how][0]
	vmin = path_link_attributes[how][1]

	tstep = get_current_timestep()
	linkids = path_link_timesteps[tstep]['linkids']
	values = path_link_timesteps[tstep][how]
	for (var i in linkids)
	{
		linkid = linkids[i]
		link_index = linkmap[linkid]
		if (link_index != undefined)
		{
		    c = values[i]
	  		color_feature(link_features[link_index], val_to_color(c, vmin, vmax));
	  	}
	}
}

function path_color_selection()
{
    if (document.getElementById('path_color_select').value == 'constant')
    	link_color_selection()
    else 
    {
    	data_selection = document.getElementById('path_data_select').value
        set_current_timestep(0)        
        color_links()
        redraw()
    }
	color_links()
  	redraw()
}

function color_links()
{
	color_features(link_features, "")
	color_features(offset_link_features, "")
		
	selected_attribute_name = document.getElementById('link_color_select').value

	if (document.getElementById("selection_type_paths").checked)
	{
		how = document.getElementById('path_color_select').value
		if (how == 'constant')
			color_features(link_features, "#ff0000")
		else
		    color_paths_by_path_attribute(how, get_current_timestep())
	}
	else if (selected_attribute_name == 'constant') 
		color_features(offset_link_features, "#ff0000")
	else 
		color_features_by_attribute(offset_link_features, linkmap, link_attributes[selected_attribute_name], get_current_timestep())
}

function link_color_selection()
{
	selected_attribute_name = document.getElementById('link_color_select').value;
	
	if (selected_attribute_name == 'constant')
		number_of_timesteps = 1
	else
		number_of_timesteps = link_attributes[selected_attribute_name].timesteps.length
		
	if (number_of_timesteps > 1)
	{
		document.getElementById('run_animation_button').disabled = false;
		document.getElementById('step_animation_button').disabled = false;
	}
	else
	{
		document.getElementById('run_animation_button').disabled = true;
		document.getElementById('step_animation_button').disabled = true;
	}
			
	set_current_timestep(0)
	color_links()
	redraw()
}

function color_nodes_by_attribute(attribute, timestep)
{
	vmin = attribute['range'][0]
	vmax = attribute['range'][1]
	
	for (var i in node_colors)
	  node_colors[i] = ''
	  
	timestep_data = attribute.data[timestep]
	
	for (var i in attribute.nodeids)
	{
	  indx = nodemap[attribute.nodeids[i]]		
	  color_features_by_attribute(node_features, nodemap, link_attributes[selected_attribute_name], get_current_timestep())
	  
	  
	  node_colors[i] = val_to_color(timestep_data[i], vmin, vmax);
	}
}

function color_nodes()
{
	selected_attribute_name = document.getElementById('node_color_select').value
	
	if (selected_attribute_name == 'constant') 
		color_features(node_features, "#ff0000")
	else
	{
	    // make sure nodes which do not have the selected attribute
	    // are not rendered
		color_features(node_features, "")
	  	color_features_by_attribute(node_features, nodemap, node_attributes[selected_attribute_name], get_current_timestep())
	}
}

function node_color_selection()
{
	selected_attribute_name = document.getElementById('node_color_select').value;
	
	if (selected_attribute_name == 'constant')
		number_of_timesteps = 1
	else
		number_of_timesteps = node_attributes[selected_attribute_name].timesteps.length
		
	if (number_of_timesteps > 1)
	{
		document.getElementById('run_animation_button').disabled = false;
		document.getElementById('step_animation_button').disabled = false;
	}
	else
	{
		document.getElementById('run_animation_button').disabled = true;
		document.getElementById('step_animation_button').disabled = true;
	}
		
	color_nodes()
	redraw()
}

function redraw()
{
    dataLayer.removeAllFeatures();
	
	features = []
	
	if (document.getElementById("selection_type_nodelink").checked)
	{		
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
	
		capacities = link_attributes['capacity']['data'][0]
		
		var radios = document.getElementsByName('capacity_level');
		min_capacity = 0
		for (var i = 0, length = radios.length; i < length && min_capacity == 0; i++) 
		    if (radios[i].checked) 
		        min_capacity = radios[i].value;
 		
		for (var i in offset_link_features)
		{
			f = offset_link_features[i]
			if (f.linkType in checkedLinkTypes && capacities[i] >= min_capacity)
				features.push(f);
		}
				
		for (var i in node_features)
		{
			n = node_features[i]
			if (n.nodeType in checkedNodeTypes)
				features.push(n)
		}
	}
	else if (document.getElementById("selection_type_busroute").checked)
	{
		busRouteCheckBoxes = document.getElementsByName('busroutes')
		checkedBusRoutes = {}
		for (var i = 0, j = busRouteCheckBoxes.length; i < j; i++)
			if (busRouteCheckBoxes[i].checked)
				checkedBusRoutes[busRouteCheckBoxes[i].value] = 1
		
		busRouteCheckBoxes = document.getElementsByName('busroutes');
		for (var i in busRouteCheckBoxes)
			if (busRouteCheckBoxes[i].checked)
			{
				route = busroutes[busRouteCheckBoxes[i].value];
				for (var l in route)
					features.push(offset_link_features[linkmap[route[l]]])
			}
	}
	else
	{	 
		if (path_mode == 0)
		{	
			popdown()
			show_popups(false)
			for (var i in path_origins)
				features.push(node_features[nodemap[path_origins[i]]]);
	    }
	    else if (path_mode == 1)
	    {
			for (var i in path_destinations)
				features.push(node_features[nodemap[path_destinations[i]]]);
	    }
	    else
	    {
	    	show_popups(true)
	    	
	    	links = path_link_timesteps[get_current_timestep()]['linkids']
	    	for (var l in links)
	    	{
	    		linkid = links[l]
	    		link_indx= linkmap[linkid]
	    		if (link_indx != undefined)
		    	    features.push(link_features[link_indx])
			}    	
  	  	}
	}

	dataLayer.addFeatures(features);
	dataLayer.redraw();        
}

function receive_link_data(data)
{
	close_dialog()
	
	if (data['status'] != 'OK')
		error_dialog('Data access error: ' + data['status']);
	else
	{
		for (var varname in data.linkdata)
		{
			attribute = data.linkdata[varname]
			attribute_minmax(attribute)
			link_attributes[varname] = attribute
		}		    
		
		post_link_color_options(varname);		
		link_color_selection();
	}
}
	
function load_link_data(filename)
{
	$.ajax({
		url: '/network/load_link_data/' + network_name + '/' + filename,
		dataType : 'json',
		cache: false,
		success: receive_link_data
		});
}

function load_link_data_dialog()
{
	open_dialog('Link Dataset', 'Do It', 'load_link_data')
}

function receive_node_data(data)
{}

function load_node_data()
{}

function receive_path_data(data)
{	
	close_dialog()
	
	if (data['status'] != 'OK')
		error_dialog('Data access error: ' + data['status']);
	else
	{
		path_datasets.push(data['dataset'])
		post_path_data_options(data['dataset'])
	}
}

function add_path_dataset(dataset)
{
	$.ajax({
		url: '/network/load_path_data/' + network_name + '/' + dataset,
		dataType : 'json',
		cache: false,
		success: receive_path_data
		});
}

function load_path_data_dialog()
{
 	open_dialog('Path Dataset', 'Do It', 'add_path_dataset')
}

function load_path_origins()
{
	$.ajax({
		url: '/network/load_origins/' + network_name + '/' + document.getElementById('path_data_select').value,
		dataType : 'json',
		cache: false,
		success: receive_path_origins
		});
}

function receive_path_origins(data)
{
	if (data['status'] != 'OK')
		error_dialog('Data access error: ' + data['status']);

    path_origins = data['origins']
    path_mode = 0
	redraw()
}

function load_path_destinations()
{
	$.ajax({
		url: '/network/load_destinations/' + network_name + '/' + document.getElementById('path_data_select').value + '/' + document.getElementById('path_origins').value,
		dataType : 'json',
		cache: false,
		success: receive_path_destinations
		});
}

function receive_path_destinations(data)
{
	if (data['status'] != 'OK')
		error_dialog('Data access error: ' + data['status']);

    path_destinations = data['destinations']
    path_mode = 1
	redraw()
}

function load_paths(o, d)
{
	$.ajax({
		url: '/network/load_paths/' + network_name + '/' + document.getElementById('path_data_select').value + '/100/' + document.getElementById('path_origins').value + '/' + document.getElementById('path_destinations').value,
		dataType : 'json',
		cache: false,
		success: receive_paths
		});
}

function receive_paths(data)
{
	if (data['status'] != 'OK')
		error_dialog('Data access error: ' + data['status']);

    set_current_timestep(0)
    
    path_link_attributes = data['data']['attributes']
    path_link_timesteps = data['data']['timesteps']
    
    number_of_timesteps = path_link_timesteps.length
    set_current_timesteps = 0
 	
 	if (number_of_timesteps > 1)
 	{
		document.getElementById('run_animation_button').disabled = false;
		document.getElementById('step_animation_button').disabled = false;
	}
	else
	{
		document.getElementById('run_animation_button').disabled = true;
		document.getElementById('step_animation_button').disabled = true;
	}

  	post_path_color_options('')
    color_links()
    path_mode = 2
	redraw()
}
function adjustSelections() {
    if (document.getElementById('selection_type_busrout').checked) {
		// get the height of control to be hidden
		var height = document.getElementById('nodeLinkTypeSelect').style.height
        $('#nodeLinkTypeSelect').animate({"left": "-=15%", "width": "-=15%"},
							    "slow"); 
		$('#busRouteSelect').animate({"top": "+=" + height.toString() + "px"}, "slow"); 
		controlsHidden = true;
	}
}
function selection_type()
{
	if (document.getElementById('selection_type_nodelink').checked)
	{
		show_popups(true)
		
		document.getElementById('pathSelect').style.visibility = "hidden"
		document.getElementById('busRouteSelect').style.visibility = "hidden"
		document.getElementById('nodeLinkTypeSelect').style.visibility = "visible"
		
		color_links()
		color_nodes()
		redraw()
	}
	else if (document.getElementById('selection_type_busroute').checked)
	{
		show_popups(true)
		
		document.getElementById('pathSelect').style.visibility = "hidden"
		document.getElementById('nodeLinkTypeSelect').style.visibility = "hidden"
		document.getElementById('busRouteSelect').style.visibility = "visible"
		
		color_links()
		color_nodes()
		redraw();
	}
	else
	{		
		show_popups(false)
		path_mode = 0
		
		//load_path_origins()
		
		document.getElementById('pathSelect').style.visibility = "visible"
		document.getElementById('nodeLinkTypeSelect').style.visibility = "hidden"
		document.getElementById('busRouteSelect').style.visibility = "hidden"
		
		document.getElementById('origin_selection_done_button').style.visibility = "visible"
		document.getElementById('origin_selection_clear_button').style.visibility = "visible"
		document.getElementById('destination_selection_clear_button').style.visibility = "hidden"
		document.getElementById('destination_selection_done_button').style.visibility = "hidden"
		document.getElementById('new_path_selection_button').style.visibility = "hidden"
		
		selectNodes()
	}
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

function change_map_intensity(v)
{
	map_intensity = map_intensity + v
	console.log(map_intensity)
	if (map_intensity >= 1.0) 
	{
		document.getElementById('mapIntensityUp').disabled = true
		document.getElementById('mapIntensityDown').disabled = false
		map_intensity = 1.0
	}
	else if (map_intensity < 0.0) 
	{
		document.getElementById('mapIntensityUp').disabled = false
		document.getElementById('mapIntensityDown').disabled = true
		map_intensity = 0.0
	}
	else
	{	
		document.getElementById('mapIntensityUp').disabled = false
		document.getElementById('mapIntensityDown').disabled = false
	}
	osm.setOpacity(map_intensity)
}

function error_dialog(message)
{   
	dlg = $( "#dialog" )
    dlg.dialog('option', 'title', 'Error!')
    dlg.html(message)
    dlg.dialog("open");
}

function close_dialog()
{
	dlg = $( "#dialog" )
    dlg.dialog("close")
}

function open_dialog(title, button_string, callback)
{	
	str = '<input type="text" id="loadfile">' +
          '<input type="button" value="' + button_string + '" ' +
          ' onclick=' + callback + '($("#loadfile").val())' +
          ' onkeydown="if (event.keyCode == 13)'  + callback + '($("#loadfile").val())' +
          '>'
           
    dlg = $( "#dialog" )
    dlg.dialog('option', 'title', title)
    dlg.html(str) 
    dlg.dialog("open")
}