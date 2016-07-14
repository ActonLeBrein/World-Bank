$(document).ready(function() {
	var id_l = [];
	search_ind();

	$('#GDN').click(function() {
		$('#NDG').slideToggle();
		$('#WBC').slideUp();
		$('#ITE').slideUp();
		$('#GPE').slideUp();
	});
	$('#CBW').click(function() {
		$('#WBC').slideToggle();
		$('#NDG').slideUp();
		$('#ITE').slideUp();
		$('#GPE').slideUp();
	});
	$('#ETI').click(function() {
		$('#ITE').slideToggle();
		$('#WBC').slideUp();
		$('#NDG').slideUp();
		$('#GPE').slideUp();
	});
	$('#EPG').click(function() {
		$('#GPE').slideToggle();
		$('#ITE').slideUp();
		$('#WBC').slideUp();
		$('#NDG').slideUp();
	});

	if ($('#KEWO').is(':visible') || $('#NDGF').is(':visible') || $('#WBCF').is(':visible') || $('#ITEF').is(':visible')) {
		$('#save_me').show();
		$('#reset_me').show();
	}
	else {
		$('#save_me').hide();
		$('#reset_me').hide();
	}
	$('.close_filter').click(function() {
		var f = $(this).siblings('.wb_ct').text();
		$('[value="'+f+'"]').remove();
		$(this).parents('li:first').remove();
		$('#main_form').submit();
	});
	$('.pagers').click(function() {
		value_page = $(this).attr("id").replace('nextpage','');
		$("input[name=page]").val(value_page);
		$("#main_form").submit();
		return false;
	});
	$('#closer').click(function() {
		$('#lightbox, #helper1, #helper2, #helper3, #helper4, #helper5, #close_helper').hide();
	})
	$('.help_opt').click(function() {
		if ($('#NORE').is(':visible')) {
			$('#lightbox, #helper3, #close_helper').show();
		}
		else if ($('#REST').is(':visible') && ($('#view_me').is(':hidden'))) {
			$('#lightbox, #helper4, #close_helper').show();
		}
		else if ($('#REST').is(':visible') && ($('#view_me').is(':visible')) && ($('#save_me').is(':hidden'))) {
			$('#lightbox, #helper5, #close_helper').show();
		}
		else if ($('#REST').is(':visible')) {
			$('#lightbox, #helper2, #close_helper').show();
		}
	})
	$('#open_helper').click(function() {
		$('#lightbox, #helper1, #close_helper').show();
	})
	$('#download_selected').click(function() {
		$("[name^=ind_sel_list]").each(function()
			{
				id_l.push($(this).val());
				$(this).remove();
			});
		location.replace('/download_indicators/?ids='+id_l);
	})
	$('#remove_selected').click(function() {
		$('#I_L_modal_body').find('.ind_list_select').remove();
		$('#buttons_ind').hide();
		$("[name^=ind_sel_list]").each(function()
			{
				$(this).remove();
			});
	})
	$('#save_selected').click(function() {
		var indic = "";
		$("input:checkbox[name=indicator_selected]:checked").each(function()
			{
				var inputh = document.createElement('input');
				inputh.type = 'hidden';
				inputh.name = 'ind_sel_list[]';
				inputh.value = $(this).val();
				$('#main_form').append(inputh);
				var t = $('#collapse'+$(this).val()).find('.descripcion')[0]['innerHTML'];
				indic += '<div class="ind_list_select"><h4><span class="badge">'+$(this).val()+'</span>'
						+'<strong style="margin-left: 5px;">Indicator Description: </strong>'+t+'</h4>'
						+'</div>'
				/*$(this).click();*/
			});
		$('#buttons_ind').before(indic);
		$('#buttons_ind').show();
	})
	$('#save_me').click(function() {
		save_query();
	})

	$('#view_me').click(function() {
		view_list();
	})
	console.log(id_l);
});

var liss = [];

function close_filter(li_li, li_re) {
	$(li_li).parents('li:first').remove();
	liss.splice(liss.indexOf(li_re), 1);
}

function search_ind() {
	var i = 0;
	var categories = [];
	var lis = "";
	$.ajax({
	url: '/rest_categories/',
	dataType : 'json',
	success: function(data) {
		$.each(data, function(index, value) {
			categories.push(value.Theme)
			lis += "<option value='"+value.Theme+"'>"+value.Theme+"</option>";
		})
		$('#combobox').html(lis);
		$("#combobox").combobox({
			source:categories,
			close:function(){
				$(".custom-combobox-input .ui-widget .ui-widget-content .ui-state-default .ui-corner-left .ui-autocomplete-input").val('');
			},
			select:function(event,ui) {
				if (liss.indexOf(ui.item.value) < 0) {
					var hidinp = document.createElement('input');
					hidinp.type = 'hidden';
					hidinp.name = 'wb_cat_list[]';
					hidinp.id = 'id_'+i;
					hidinp.value = ui.item.value;

					var a_close = document.createElement('a');
					a_close.href = '#';
					a_close.innerHTML = '<span class="glyphicon glyphicon-remove-sign"></span></li>';
					$(a_close).click(function() {
						close_filter(a_close, ui.item.value)
					});

					var li_f = document.createElement('li');
					li_f.innerHTML = '<span class="wb_ct">'+ui.item.value+'</span>';
					$(li_f).append(a_close);
					$(li_f).append(hidinp);

					$('#wb_filters').append(li_f);

					i += 1;
					liss.push(ui.item.value);
				}
			}
		});
	}
	});
}

function save_query() {
	var	datapost = $('#main_form').serializeArray();
	$.ajax({
		url: '/save/',
		data: datapost,
		type: 'post',
		success: function(data) {
			$('#Q_L_modal_body').empty();
			var query = "";
			for (i = 0; i < data.length; i++) {
				if (i == data.length - 1) {
					query += '<div id="q_'+i+'""><h4><span class="badge">'+(i+1)+'</span>'
							+'<strong> Keyword Search: </strong>'+data[i][1]['key_se_list[]']+'<br>'
							+'<strong class="q_l"> New Deal Goal: </strong>'+data[i][2]['nw_dg_list[]']+'<br>'
							+'<strong class="q_l"> World Bank Category: </strong>'+data[i][3]['wb_cat_list[]']+'<br>'
							+'<strong class="q_l"> Indicator Type: </strong>'+data[i][4]['in_tp_list[]']+'</h4><br>'
							+'<button type="button" class="down_q btn btn-danger">Download<span class="glyphicon glyphicon-download-alt"></span></button>'
							+'<button type="button" class="remove_q btn btn-danger">Remove<span class="glyphicon glyphicon-remove"></span></button>'
							+'</div>'
				}
				else {
					query += '<div id="q_'+i+'""><h4><span class="badge">'+(i+1)+'</span>'
							+'<strong> Keyword Search: </strong>'+data[i][1]['key_se_list[]']+'<br>'
							+'<strong class="q_l"> New Deal Goal: </strong>'+data[i][2]['nw_dg_list[]']+'<br>'
							+'<strong class="q_l"> World Bank Category: </strong>'+data[i][3]['wb_cat_list[]']+'<br>'
							+'<strong class="q_l"> Indicator Type: </strong>'+data[i][4]['in_tp_list[]']+'</h4><br>'
							+'<button type="button" class="down_q btn btn-danger">Download<span class="glyphicon glyphicon-download-alt"></span></button>'
							+'<button type="button" class="remove_q btn btn-danger">Remove<span class="glyphicon glyphicon-remove"></span></button>'
							+'</div><hr>'
				}
			}
			$('#Q_L_modal_body').html(query);
			$('.remove_q').click(function() {
				var div_q = $(this).parents('div:first');
				var id_q = $(div_q).attr('id').replace('q_','');
				remove_query(id_q);
			});
			$('.down_q').click(function() {
				var div_q = $(this).parents('div:first');
				var id_q = $(div_q).attr('id').replace('q_','');
				location.replace('/download_query/'+id_q);
			});
		}
	});
}

function view_list() {
	$.ajax({
		url: '/view_list/',
		dataType : 'json',
		success: function(data) {
			$('#Q_L_modal_body').empty();
			var query = "";
			for (i = 0; i < data.length; i++) {
				if (i == data.length - 1) {
					query += '<div id="q_'+i+'""><h4><span class="badge">'+(i+1)+'</span>'
							+'<strong> Keyword Search: </strong>'+data[i][1]['key_se_list[]']+'<br>'
							+'<strong class="q_l"> New Deal Goal: </strong>'+data[i][2]['nw_dg_list[]']+'<br>'
							+'<strong class="q_l"> World Bank Category: </strong>'+data[i][3]['wb_cat_list[]']+'<br>'
							+'<strong class="q_l"> Indicator Type: </strong>'+data[i][4]['in_tp_list[]']+'</h4><br>'
							+'<button type="button" class="down_q btn btn-danger">Download<span class="glyphicon glyphicon-download-alt"></span></button>'
							+'<button type="button" class="remove_q btn btn-danger">Remove<span class="glyphicon glyphicon-remove"></span></button>'
							+'</div>'
				}
				else {
					query += '<div id="q_'+i+'""><h4><span class="badge">'+(i+1)+'</span>'
							+'<strong> Keyword Search: </strong>'+data[i][1]['key_se_list[]']+'<br>'
							+'<strong class="q_l"> New Deal Goal: </strong>'+data[i][2]['nw_dg_list[]']+'<br>'
							+'<strong class="q_l"> World Bank Category: </strong>'+data[i][3]['wb_cat_list[]']+'<br>'
							+'<strong class="q_l"> Indicator Type: </strong>'+data[i][4]['in_tp_list[]']+'</h4><br>'
							+'<button type="button" class="down_q btn btn-danger">Download<span class="glyphicon glyphicon-download-alt"></span></button>'
							+'<button type="button" class="remove_q btn btn-danger">Remove<span class="glyphicon glyphicon-remove"></span></button>'
							+'</div><hr>'
				}
			}
			$('#Q_L_modal_body').html(query);
			$('.remove_q').click(function() {
				var div_q = $(this).parents('div:first');
				var id_q = $(div_q).attr('id').replace('q_','');
				remove_query(id_q);
			});
			$('.down_q').click(function() {
				var div_q = $(this).parents('div:first');
				var id_q = $(div_q).attr('id').replace('q_','');
				location.replace('/download_query/'+id_q);
			});
		}
	});
}

function remove_query(id_q) {
	var id = id_q;
	$.ajax({
		url: '/remove_query/',
		data: {'id':id, csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()},
		type: 'post',
		success: function(data) {
			$('#Q_L_modal_body').empty();
			var query = "";
			for (i = 0; i < data.length; i++) {
				if (i == data.length - 1) {
					query += '<div id="q_'+i+'""><h4><span class="badge">'+(i+1)+'</span>'
							+'<strong> Keyword Search: </strong>'+data[i][1]['key_se_list[]']+'<br>'
							+'<strong class="q_l"> New Deal Goal: </strong>'+data[i][2]['nw_dg_list[]']+'<br>'
							+'<strong class="q_l"> World Bank Category: </strong>'+data[i][3]['wb_cat_list[]']+'<br>'
							+'<strong class="q_l"> Indicator Type: </strong>'+data[i][4]['in_tp_list[]']+'</h4><br>'
							+'<button type="button" class="down_q btn btn-danger">Download<span class="glyphicon glyphicon-download-alt"></span></button>'
							+'<button type="button" class="remove_q btn btn-danger">Remove<span class="glyphicon glyphicon-remove"></span></button>'
							+'</div>'
				}
				else {
					query += '<div id="q_'+i+'""><h4><span class="badge">'+(i+1)+'</span>'
							+'<strong> Keyword Search: </strong>'+data[i][1]['key_se_list[]']+'<br>'
							+'<strong class="q_l"> New Deal Goal: </strong>'+data[i][2]['nw_dg_list[]']+'<br>'
							+'<strong class="q_l"> World Bank Category: </strong>'+data[i][3]['wb_cat_list[]']+'<br>'
							+'<strong class="q_l"> Indicator Type: </strong>'+data[i][4]['in_tp_list[]']+'</h4><br>'
							+'<button type="button" class="down_q btn btn-danger">Download<span class="glyphicon glyphicon-download-alt"></span></button>'
							+'<button type="button" class="remove_q btn btn-danger">Remove<span class="glyphicon glyphicon-remove"></span></button>'
							+'</div><hr>'
				}
			}
			$('#Q_L_modal_body').html(query);
			$('.remove_q').click(function() {
				var div_q = $(this).parents('div:first');
				var id_q = $(div_q).attr('id').replace('q_','');
				remove_query(id_q);
			});
			$('.down_q').click(function() {
				var div_q = $(this).parents('div:first');
				var id_q = $(div_q).attr('id').replace('q_','');
				location.replace('/download_query/'+id_q);
			});
		}
	});
}

$(function() {
	$( "#combobox" ).combobox();
});