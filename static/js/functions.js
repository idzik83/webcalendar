$.ajaxSetup({ 
	beforeSend: function(xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
	                if (cookie.substring(0, name.length + 1) == (name + '=')) {
	                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	                    break;
                 	}
         		}
         	}
        return cookieValue;
        }
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
     	}
 	} 
});

$(document).ready(function () {
	$('#cancel').click(function () {
		$('.collapse').collapse('hide');
	})
})

$(document).ready(function () {
	$('#save').click(function () {
		var data = {};
		var eventList = [];

		$.each($('input'), function (index, argument) {
			if (argument.type == 'text') {
				dataObj = {};
				dataObj['event'] = argument.value;
				dataObj['id'] = argument.id;
				eventList.push(dataObj);
			}
		});
		data['events'] = eventList;
		data['date_event'] = cur_id;
		$.ajax({
			type: 'POST',
			url: 'save',
			dataType: "json",
			data: JSON.stringify(data),
			success: function () {
				clearForm();
				window.location.href = '/';
			}
		});
	})
})

$(document).ready(function() {
	$('#cancel').click(function(event) {
		event.stopPropagation();
		event.preventDefault();
		$('.collapse').collapse('hide');
	})
})

var cur_id = 0;
function rollout(element) {
	clearForm();
	var position = $('.collapse').position();
	if (element.className != 'col-md-1 not_cur_month') {
		cur_id = element.id
		var day = element.childNodes[1].innerHTML;
		data = {}
		data['date'] = cur_id;
		$.ajax({
			type: 'POST',
			url: 'geteventlist',
			dataType: "json",
			data: JSON.stringify(data),
			success: function (data) {
				$.each(data, function (index, argument) {
					addEvent(argument['event'], argument['event_id']);
				});
				$('.collapse').collapse('toggle');
			}
		});
	} else return;
}

function clearForm() {
	$.each($('.panel-body'), function (index, argument) {
		argument.remove();
	});
}

function addEvent(eventName, eventId) {
	document.forms[0].appendChild(createPanel(eventName, eventId));
}

function delEvent (element) {
	var eventID = {}
	eventID['id'] = element.getAttribute('data-event-id');
	eventID['date'] = cur_id;
	$.ajax({
		type: 'POST',
		url: 'delevent',
		dataType: "json",
		data: JSON.stringify(eventID),
		success: function () {
			element.parentNode.parentNode.parentNode.remove();
		}
	});
}

function createPanel (eventName, eventId) {
	var panelNode = document.createElement('div');
	var rowNode  = document.createElement('div');
	var col7Node = document.createElement('div');
	var col2Node = document.createElement('div');
	var inputNode = document.createElement('input');
	var buttonNode = document.createElement('button');
	var labelNode = document.createElement('label');
	panelNode.className = 'panel-body';
	rowNode.className = 'row';
	col7Node.className = 'col-md-7';
	col2Node.className = 'col-md-2';
	inputNode.className = 'form-control';
	if (typeof eventName === 'undefined') {
		inputNode.value = "";
	} else {
		inputNode.value = eventName;
		inputNode.id = eventId;
		buttonNode.setAttribute('data-event-id', eventId)
	}
	buttonNode.setAttribute('onclick', 'delEvent(this)');
	buttonNode.className = 'btn btn-primary btn-md';
	buttonNode.id = 'del';
	buttonNode.type = 'button';
	buttonNode.textContent = 'Удалить';
	labelNode.setAttribute('for', inputNode.id);
	col2Node.appendChild(buttonNode);
	col7Node.appendChild(inputNode);
	rowNode.appendChild(col7Node);
	rowNode.appendChild(col2Node);
	panelNode.appendChild(labelNode);
	panelNode.appendChild(rowNode);
	return panelNode;
}

function getDateID () {
	var year = document.getElementById("year").innerHTML;
	var month = document.getElementById("month").innerHTML;
	return cur_day + month + year;
}
