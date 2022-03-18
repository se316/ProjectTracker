// update status icons when the selected status is changed

function update_status_icons () {
	// get all the entry items on the page
	var icons = document.getElementsByClassName('current-icon');
	var statuses = document.getElementsByClassName('current-status');
	for (i=0; i<icons.length; i++) {
		try {
		        var icon = icons[i];
		        var status = statuses[i].selectedOptions[0].text;
		        update_icon(icon, status);
		}
		catch (e) {
		        console.log(e);
		}
	}
}

// control structure for setting the appropriate class names

function update_icon(icon, status) {
    // set the appropriate icon based on status
	var dark = '#393e46';
	var light = '#fffdf6';
        if (status == 'Not Started') {
            icon.className = 'current-icon fa-solid fa-box';
	    icon.style.background = '#929aab';
	    icon.style.color = light;
        } else if (status == 'Pending') {
            icon.className = 'current-icon fa-solid fa-circle-pause';
            icon.style.background = '#962071';
            icon.style.color = light;
        } else if (status == 'In Progress') {
            icon.className = 'current-icon fa-solid fa-box-open';
            icon.style.background = '#00aaa0';
            icon.style.color = light;
        } else if (status == 'Review') {
            icon.className = 'current-icon fa-solid fa-landmark';
            icon.style.background = '#ffc93c';
            icon.style.color = light;
        } else if (status == 'Complete') {
            icon.className = 'current-icon fa-solid fa-circle-check';
            icon.style.background = '#a2c11c';
            icon.style.color = light;
        }
    }

// update a project or subtask status with fetch

function update_status(lvl, id, formid) {
	// get form data
	var form = document.getElementById(formid);
	var data = new FormData(form);

	// fetch request
	var url = '/edit/status/' + lvl + '/' + id;
	fetch(url, {
		method: 'POST',
		body: data})
	.then((res) => { return res.text(); })
	.then((txt) => { console.log(txt); })
	.catch((err) => { console.log(err); });

	// prevent page refresh
	return false
}
		

// toggle b/w project and subtask view

function toggle_view(view) {
	// elements to target
	const proj = document.getElementById('project_view');
	const st = document.getElementById('subtask_view');

	// used for setting the active tab
	const tabs = document.getElementsByClassName('tabs')[0];
	const p = tabs.children[0]; // project tab
	const s = tabs.children[1]; // subtask tab
	const active_bg = '#e0e0e0';
	const regular_bg = 'inherit';

	if (view == 'project_view') {
		// set project view as visible
		proj.style.display = 'block';
		p.className = 'active';
		p.style.backgroundColor = active_bg;

		st.style.display = 'none';
		s.className = '';
		s.style.backgroundColor = regular_bg;

	} else if (view == 'subtask_view') {
		proj.style.display = 'none';
		p.className = '';
		p.style.backgroundColor = regular_bg;

		st.style.display = 'block';
		s.className = 'active';
		s.style.backgroundColor = active_bg;
	}
}

// confirmation dialogue for deleting

function confirm_delete(lvl, id) {
	// url syntax should always be /delete/<lvl>/<id>
	// lvl is one of: project, subtask, comment
	// id is the unique id for the lvl you're trying to delete
	var msg = 'You are about to delete a ' + lvl +'. This cannot be undone.';
	if (confirm(msg)) {
		var loc = '/delete/' + lvl + '/' + id;
		window.location = loc;
	}
}


// toggle element visibility

function show_hide(div_name) {
	var ele = document.getElementById(div_name);
	if (ele.style.display == 'none') {
		ele.style.display = 'block'; }
	else {
		ele.style.display = 'none';
	}
}

// open docs and explanation for what markdown is and which is used

function markdown_help() {
	var sites = ['https://github.github.com/gfm/','https://becomeawritertoday.com/what-is-markdown/#What_Is_Markdown'];

	for (i=0; i<sites.length; i++) {
		window.open(sites[i], '_blank');
	}
}

// func to render markdown. Make this flexible so it works beyond the project lvl

function convert_md(txt_id) {
	const md = new Remarkable('full', {gfm:true});
	var txt_in = document.getElementById(txt_id);
	var target = document.getElementById('preview');

	// display current text rendered into the preview section
	target.innerHTML = md.render(txt_in.value);
}
