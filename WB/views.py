from django.shortcuts import render_to_response, redirect, render
from django.http import *
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf
from WB.models import *
from sets import Set
from django.core import serializers
#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
import csv
import simplejson
# Create your views here.

def home(request, template_name = 'main.html'):
	res_post = False
	try:
		if len(request.session['posts']) > 0:
			res_post = True
	except:
		res_post = False
	try:
		ind_list = Indicator.objects.order_by('Description')
	except Indicator.DoesNotExist:
		ind_list = True

	if not ind_list == True:
		paginator = Paginator(ind_list, 20)
		page = request.POST.get('page',1)
		try:
			indicators = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			indicators = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			indicators = paginator.page(paginator.num_pages)
		args = {}
		args.update(csrf(request))
		args['indicators'] = indicators
		args['res_post'] = res_post
		return render(request, template_name, args)
	else:
		posts = [{'page':'1'}]
		args = {}
		args.update(csrf(request))
		args['all_posts'] = posts
		args['res_post'] = res_post
		return render(request, template_name, args)

def upload(request):
	Categories_pbsb = ['n/a','Political Legitimacy','Security','Justice','Economic Foundations','Revenues & Services']
	filesource = '/opt/myenv/world-bank/WB/static/WB_CSV/140612_WB_Indicators_3.csv'
	with open(filesource, 'rb') as f:
		reader = csv.reader(f, delimiter = ',', quotechar='"')
		reader.next()
		for row in reader:

			country = row[7]
			if country != '':
				new_country,fail_country = Indicator_Country.objects.get_or_create(Country = country)
			else:
				new_country,fail_country = Indicator_Country.objects.get_or_create(Country = 'n/a')

			wb_categ = row[5]
			if wb_categ != '':
				new_wb_categ,fail_wb_categ = WB_Category.objects.get_or_create(Theme = wb_categ)
			else:
				new_wb_categ,fail_wb_categ = WB_Category.objects.get_or_create(Theme = 'n/a')

			ind_type = row[6]
			if ind_type != '':
				new_ind_type,fail_ind_type = Indicator_Type.objects.get_or_create(Type = ind_type)
			else:
				new_ind_type,fail_ind_type = Indicator_Type.objects.get_or_create(Type = 'n/a')

			if row[4] != 'n/a':
				pbsbs = row[4].split(',')
				val_pbsb = ['%s'%(Categories_pbsb[int(x)]) for x in pbsbs]
				val_pbsb = ', '.join(val_pbsb)
			else:
				val_pbsb = Categories_pbsb[0]

			if row[2] != '':
				if row[5] != '':
					if row[6] != '':
						if row[7] != '':
							new_indicator = Indicator.objects.create(Description = row[1],
																	Quality = row[2],
																	DataSets_Availables = row[3],
																	PBSB = val_pbsb,
																	Source = row[8],
																	ID_WB_Category = WB_Category.objects.get(Theme = row[5]),
																	ID_Indicator_Type = Indicator_Type.objects.get(Type = row[6]),
																	ID_Indicator_Country = Indicator_Country.objects.get(Country = row[7])
																	)
						else:
							new_indicator = Indicator.objects.create(Description = row[1],
																	Quality = row[2],
																	DataSets_Availables = row[3],
																	PBSB = val_pbsb,
																	Source = row[8],
																	ID_WB_Category = WB_Category.objects.get(Theme = row[5]),
																	ID_Indicator_Type = Indicator_Type.objects.get(Type = row[6]),
																	ID_Indicator_Country = Indicator_Country.objects.get(Country = 'n/a')
																	)
					else:
						if row[7] != '':
							new_indicator = Indicator.objects.create(Description = row[1],
																	Quality = row[2],
																	DataSets_Availables = row[3],
																	PBSB = val_pbsb,
																	Source = row[8],
																	ID_WB_Category = WB_Category.objects.get(Theme = row[5]),
																	ID_Indicator_Type = Indicator_Type.objects.get(Type = 'n/a'),
																	ID_Indicator_Country = Indicator_Country.objects.get(Country = row[7])
																	)
						else:
							new_indicator = Indicator.objects.create(Description = row[1],
																	Quality = row[2],
																	DataSets_Availables = row[3],
																	PBSB = val_pbsb,
																	Source = row[8],
																	ID_WB_Category = WB_Category.objects.get(Theme = row[5]),
																	ID_Indicator_Type = Indicator_Type.objects.get(Type = 'n/a'),
																	ID_Indicator_Country = Indicator_Country.objects.get(Country = 'n/a')
																	)
				else:
					if row[6] != '':
						if row[7] != '':
							new_indicator = Indicator.objects.create(Description = row[1],
																	Quality = row[2],
																	DataSets_Availables = row[3],
																	PBSB = val_pbsb,
																	Source = row[8],
																	ID_WB_Category = WB_Category.objects.get(Theme = 'n/a'),
																	ID_Indicator_Type = Indicator_Type.objects.get(Type = row[6]),
																	ID_Indicator_Country = Indicator_Country.objects.get(Country = row[7])
																	)
						else:
							new_indicator = Indicator.objects.create(Description = row[1],
																	Quality = row[2],
																	DataSets_Availables = row[3],
																	PBSB = val_pbsb,
																	Source = row[8],
																	ID_WB_Category = WB_Category.objects.get(Theme = 'n/a'),
																	ID_Indicator_Type = Indicator_Type.objects.get(Type = row[6]),
																	ID_Indicator_Country = Indicator_Country.objects.get(Country = 'n/a')
																	)
					else:
						if row[7] != '':
							new_indicator = Indicator.objects.create(Description = row[1],
																	Quality = row[2],
																	DataSets_Availables = row[3],
																	PBSB = val_pbsb,
																	Source = row[8],
																	ID_WB_Category = WB_Category.objects.get(Theme = 'n/a'),
																	ID_Indicator_Type = Indicator_Type.objects.get(Type = 'n/a'),
																	ID_Indicator_Country = Indicator_Country.objects.get(Country = row[7])
																	)
						else:
							new_indicator = Indicator.objects.create(Description = row[1],
																	Quality = row[2],
																	DataSets_Availables = row[3],
																	PBSB = val_pbsb,
																	Source = row[8],
																	ID_WB_Category = WB_Category.objects.get(Theme = 'n/a'),
																	ID_Indicator_Type = Indicator_Type.objects.get(Type = 'n/a'),
																	ID_Indicator_Country = Indicator_Country.objects.get(Country = 'n/a')
																	)
			else:
				if row[5] != '':
					if row[6] != '':
						if row[7] != '':
							new_indicator = Indicator.objects.create(Description = row[1],
																	Quality = 'n/a',
																	DataSets_Availables = row[3],
																	PBSB = val_pbsb,
																	Source = row[8],
																	ID_WB_Category = WB_Category.objects.get(Theme = row[5]),
																	ID_Indicator_Type = Indicator_Type.objects.get(Type = row[6]),
																	ID_Indicator_Country = Indicator_Country.objects.get(Country = row[7])
																	)
						else:
							new_indicator = Indicator.objects.create(Description = row[1],
																	Quality = 'n/a',
																	DataSets_Availables = row[3],
																	PBSB = val_pbsb,
																	Source = row[8],
																	ID_WB_Category = WB_Category.objects.get(Theme = row[5]),
																	ID_Indicator_Type = Indicator_Type.objects.get(Type = row[6]),
																	ID_Indicator_Country = Indicator_Country.objects.get(Country = 'n/a')
																	)
					else:
						if row[7] != '':
							new_indicator = Indicator.objects.create(Description = row[1],
																	Quality = 'n/a',
																	DataSets_Availables = row[3],
																	PBSB = val_pbsb,
																	Source = row[8],
																	ID_WB_Category = WB_Category.objects.get(Theme = row[5]),
																	ID_Indicator_Type = Indicator_Type.objects.get(Type = 'n/a'),
																	ID_Indicator_Country = Indicator_Country.objects.get(Country = row[7])
																	)
						else:
							new_indicator = Indicator.objects.create(Description = row[1],
																	Quality = 'n/a',
																	DataSets_Availables = row[3],
																	PBSB = val_pbsb,
																	Source = row[8],
																	ID_WB_Category = WB_Category.objects.get(Theme = row[5]),
																	ID_Indicator_Type = Indicator_Type.objects.get(Type = 'n/a'),
																	ID_Indicator_Country = Indicator_Country.objects.get(Country = 'n/a')
																	)
				else:
					if row[6] != '':
						if row[7] != '':
							new_indicator = Indicator.objects.create(Description = row[1],
																	Quality = 'n/a',
																	DataSets_Availables = row[3],
																	PBSB = val_pbsb,
																	Source = row[8],
																	ID_WB_Category = WB_Category.objects.get(Theme = 'n/a'),
																	ID_Indicator_Type = Indicator_Type.objects.get(Type = row[6]),
																	ID_Indicator_Country = Indicator_Country.objects.get(Country = row[7])
																	)
						else:
							new_indicator = Indicator.objects.create(Description = row[1],
																	Quality = 'n/a',
																	DataSets_Availables = row[3],
																	PBSB = val_pbsb,
																	Source = row[8],
																	ID_WB_Category = WB_Category.objects.get(Theme = 'n/a'),
																	ID_Indicator_Type = Indicator_Type.objects.get(Type = row[6]),
																	ID_Indicator_Country = Indicator_Country.objects.get(Country = 'n/a')
																	)
					else:
						if row[7] != '':
							new_indicator = Indicator.objects.create(Description = row[1],
																	Quality = 'n/a',
																	DataSets_Availables = row[3],
																	PBSB = val_pbsb,
																	Source = row[8],
																	ID_WB_Category = WB_Category.objects.get(Theme = 'n/a'),
																	ID_Indicator_Type = Indicator_Type.objects.get(Type = 'n/a'),
																	ID_Indicator_Country = Indicator_Country.objects.get(Country = row[7])
																	)
						else:
							new_indicator = Indicator.objects.create(Description = row[1],
																	Quality = 'n/a',
																	DataSets_Availables = row[3],
																	PBSB = val_pbsb,
																	Source = row[8],
																	ID_WB_Category = WB_Category.objects.get(Theme = 'n/a'),
																	ID_Indicator_Type = Indicator_Type.objects.get(Type = 'n/a'),
																	ID_Indicator_Country = Indicator_Country.objects.get(Country = 'n/a')
																	)

			if row[9] != '':
				new_comment = Indicator_Comments.objects.create(ID_Indicator = new_indicator, Comment = row[9])

			if row[10] != '':
				new_note = Indicator_Notes.objects.create(ID_Indicator = new_indicator, Note = row[10])
	return redirect('/')

def search_main(keyword):
	k = []
	if type(keyword) == list:
		for i in keyword:
			k = k + i.split(' ') + [i]
	else:
		k = keyword.split(' ') + [keyword]
	try:
		kwards = {}
		args = Q()
		for x in k:
			y = ' %s ' %(x)
			args.add(Q(Description__icontains = y)|
					 Q(Quality__icontains = y)|
					 Q(PBSB__icontains = y)|
					 Q(Source__icontains = y)|
					 Q(ID_WB_Category__Theme__icontains = y)|
					 Q(ID_Indicator_Type__Type__icontains = y)|
					 Q(ID_Indicator_Country__Country__icontains = y)|
					 Q(indicator_comments__Comment__icontains = y)|
					 Q(indicator_notes__Note__icontains = y), Q.OR)

		ind_list = Indicator.objects.filter(*[args], **kwards).order_by('Description').distinct()
	except Indicator.DoesNotExist:
		pass
	return ind_list

def filter_main(filter_list, filter_type, filters):
	filter_res = []

	if len(filter_list) != 0:
		if filter_type == 'ng_filter':
			for i in filter_list:
				if  len(sorted(set(map(str,i.PBSB.split(','))) & set(filters))) > 0:
					filter_res = filter_res + [i]
			# try:
			# 	filter_res = filter_list.filter(PBSB__in = filters).order_by('Description')
			# except Indicator.DoesNotExist:
			# 	filter_res = []
		elif filter_type == 'wb_filter':
			for j in filter_list:
				if str(j.ID_WB_Category) in filters:
					filter_res = filter_res + [j]
			# try:
			# 	filter_res = filter_list.filter(ID_WB_Category__Theme__in = filters).order_by('Description')
			# except Indicator.DoesNotExist:
			# 	filter_res = []
		else:
			for k in filter_list:
				if str(k.ID_Indicator_Type) in filter_list:
					filter_res = filter_res + [k]
			# try:
			# 	filter_res = filter_list.filter(ID_Indicator_Type__Type__in = filters).order_by('Description')
			# except Indicator.DoesNotExist:
			# 	filter_res = []
		return filter_res
	else:
		filter_list = Indicator.objects.order_by('Description')
		if filter_type == 'ng_filter':
			try:
				filter_res = filter_list.filter(PBSB__in = filters).order_by('Description')
			except Indicator.DoesNotExist:
				filter_res = []
		elif filter_type == 'wb_filter':
			try:
				filter_res = filter_list.filter(ID_WB_Category__Theme__in = filters).order_by('Description')
			except Indicator.DoesNotExist:
				filter_res = []
		else:
			try:
				filter_res = filter_list.filter(ID_Indicator_Type__Type__in = filters).order_by('Description')
			except Indicator.DoesNotExist:
				filter_res = []
		return filter_res

def main(request, template_name = 'main.html'):

	############
	#  SEARCH  #
	############
	try:
		keywords = request.POST['keywords'].encode("utf-8")
	except:
		keywords = []

	######################
	#  PREVIEWS SEARCHS  #
	######################
	keywords_list = request.POST.getlist('key_se_list[]')
	keywords_list = map(str, keywords_list)

	#############
	#  FILTERS  #
	#############
	ng_filter = request.POST.getlist('nw_dg_list[]')
	ng_filter = map(str, ng_filter)
	ng_filter = sorted(set(ng_filter))

	wb_filter = request.POST.getlist('wb_cat_list[]')
	wb_filter = map(str, wb_filter)
	wb_filter = sorted(set(wb_filter))

	it_filter = request.POST.getlist('in_tp_list[]')
	it_filter = map(str, it_filter)
	it_filter = sorted(set(it_filter))

	#########################
	#  INDICATORS SELECTED  #
	#########################

	ind_sel = request.POST.getlist('ind_sel_list[]')
	ind_sel = map(int, ind_sel)
	ind_sel = sorted(set(ind_sel))
	des = []
	if len(ind_sel) != 0:
		for i in ind_sel:
			des = des + [Indicator.objects.get(id = i)]
	ind_sel = map(str, ind_sel)
	ind_sel = sorted(set(ind_sel))
	
	##################
	#  FINAL RESULT  #
	##################
	res= []

	if len(keywords) != 0:
		res = search_main(keywords)
	
	if len(keywords_list) != 0:
		res = search_main(keywords_list)

	if len(ng_filter) != 0:
		res = filter_main(res, 'ng_filter', ng_filter)

	if len(wb_filter) != 0:
		res = filter_main(res, 'wb_filter', wb_filter)

	if len(it_filter) != 0:
		res = filter_main(res, 'it_filter', it_filter)

	if len(keywords) != 0:
		keywords_list = keywords_list + [keywords]
		keywords_list = sorted(set(keywords_list))

	####################################################################################################################################################################
	posts = [{'page':'1'},{'key_se_list[]':keywords_list},{'nw_dg_list[]':ng_filter},{'wb_cat_list[]':wb_filter},{'in_tp_list[]':it_filter},{'ind_sel_list[]':ind_sel}]
	####################################################################################################################################################################

	if (len(keywords_list) == 0) & (len(ng_filter) == 0) & (len(wb_filter) == 0) & (len(it_filter) == 0):
		flag = True
	else:
		flag = False

	if len(res) != 0:
		paginator = Paginator(res, 20)
		page = request.POST.get('page',1)
		try:
			indicators = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			indicators = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			indicators = paginator.page(paginator.num_pages)
		args = {}
		args.update(csrf(request))
		args['indicators'] = indicators
		args['key_se_list'] = keywords_list
		args['ng_filter'] = ng_filter
		args['wb_filter'] = wb_filter
		args['it_filter'] = it_filter
		args['all_posts'] = posts
		args['des'] = des
		args['res_post'] = True
		args['matches'] = len(res)
		return render(request, template_name, args)
	elif flag == False:
		paginator = Paginator(res, 20)
		page = request.POST.get('page',1)
		try:
			indicators = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			indicators = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			indicators = paginator.page(paginator.num_pages)
		args = {}
		args.update(csrf(request))
		args['indicators'] = indicators
		args['key_se_list'] = keywords_list
		args['ng_filter'] = ng_filter
		args['wb_filter'] = wb_filter
		args['it_filter'] = it_filter
		args['all_posts'] = posts
		args['des'] = des
		args['res_post'] = True
		args['no_results'] = True
		return render(request, template_name, args)
	else:
		try:
			ind_list = Indicator.objects.order_by('Description')
		except Indicator.DoesNotExist:
			ind_list = True
		if not ind_list == True:
			paginator = Paginator(ind_list, 20)
			page = request.POST.get('page',1)
			try:
				indicators = paginator.page(page)
			except PageNotAnInteger:
				# If page is not an integer, deliver first page.
				indicators = paginator.page(1)
			except EmptyPage:
				# If page is out of range (e.g. 9999), deliver last page of results.
				indicators = paginator.page(paginator.num_pages)
			posts = [{'page':'1'}]
			args = {}
			args.update(csrf(request))
			args['indicators'] = indicators
			args['all_posts'] = posts
			args['des'] = des
			args['res_post'] = False
			return render(request, template_name, args)

def view_list(request):
	data = simplejson.dumps(request.session['posts'])
	return HttpResponse(data, content_type="application/json")

def save(request):

	############
	#  SEARCH  #
	############
	try:
		keywords = request.POST['keywords'].encode("utf-8")
	except:
		keywords = []

	######################
	#  PREVIEWS SEARCHS  #
	######################
	keywords_list = request.POST.getlist('key_se_list[]')
	keywords_list = map(str, keywords_list)

	#############
	#  FILTERS  #
	#############
	ng_filter = request.POST.getlist('nw_dg_list[]')
	ng_filter = map(str, ng_filter)
	ng_filter = sorted(set(ng_filter))

	wb_filter = request.POST.getlist('wb_cat_list[]')
	wb_filter = map(str, wb_filter)
	wb_filter = sorted(set(wb_filter))

	it_filter = request.POST.getlist('in_tp_list[]')
	it_filter = map(str, it_filter)
	it_filter = sorted(set(it_filter))

	##################
	#  FINAL RESULT  #
	##################
	res= []

	if len(keywords) != 0:
		res = search_main(keywords)
	
	if len(keywords_list) != 0:
		res = search_main(keywords_list)

	if len(ng_filter) != 0:
		res = filter_main(res, 'ng_filter', ng_filter)

	if len(wb_filter) != 0:
		res = filter_main(res, 'wb_filter', wb_filter)

	if len(it_filter) != 0:
		res = filter_main(res, 'it_filter', it_filter)

	if len(keywords) != 0:
		keywords_list = keywords_list + [keywords]
		keywords_list = sorted(set(keywords_list))

	########################################################################################################################################
	posts = [{'page':'1'},{'key_se_list[]':keywords_list},{'nw_dg_list[]':ng_filter},{'wb_cat_list[]':wb_filter},{'in_tp_list[]':it_filter}]
	########################################################################################################################################
	try:
		request.session['posts'] = request.session['posts'] + [posts]
	except:
		request.session['posts'] = [posts]
	########################################################################################################################################
	data = simplejson.dumps(request.session['posts'])
	return HttpResponse(data, content_type="application/json")

def remove_query(request):
	pos = request.POST['id'].encode("utf-8")
	pos = int(pos)

	del request.session['posts'][pos]

	request.session['posts'] = request.session['posts']
	data = simplejson.dumps(request.session['posts'])
	return HttpResponse(data, content_type="application/json")

def download_query(request, id_q):
	pos = id_q.encode("utf-8")
	pos = int(pos)

	q = request.session['posts'][pos]

	q1 = map(str, q[1]['key_se_list[]'])
	q2 = map(str, q[2]['nw_dg_list[]'])
	q3 = map(str, q[3]['wb_cat_list[]'])
	q4 = map(str, q[4]['in_tp_list[]'])

	##################
	#  FINAL RESULT  #
	##################
	res = []

	if len(q1) != 0:
		res = search_main(q1)

	if len(q2) != 0:
		res = filter_main(res, 'ng_filter', q2)

	if len(q3) != 0:
		res = filter_main(res, 'wb_filter', q3)

	if len(q4) != 0:
		res = filter_main(res, 'it_filter', q4)

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="download.csv"'
	writer = csv.writer(response)
	writer.writerow(['(0) Index','(1) INDICATOR (n)','(2) INDICATOR QUALITY (3) (g, y, r)','(3) DATASETS AVAILABLE (Hyperlink)','(4) PBSB CATEGORY (5) ((1, 2, 3, 4, 5))','(5) WB CATEGORY (Theme)','(6) INDICATOR TYPE (2) (SbPb, Ops)','(7) INDICATOR COUNTRY (or region)(n=129 (incl 7 regions) (193)','(8) INDICATOR SOURCE','(9) COMMENTS (n)','(10) Notes'])
	for i in range(0, len(res)):
		if len(res[i].indicator_comments_set.all()) == 0:
			a = 'n/a'
		else:
			a = res[i].indicator_comments_set.all()[0]
		if len(res[i].indicator_notes_set.all()) == 0:
			b = 'n/a'
		else:
			b = res[i].indicator_notes_set.all()[0]
		if res[i].Description == None:
			c = 'n/a'
		else:
			c = res[i].Description
		if res[i].DataSets_Availables == None:
			d = 'n/a'
		else:
			d = res[i].DataSets_Availables
		if len(res[i].indicator_notes_set.all()) == 0:
			e = 'n/a'
		else:
			e = res[i].indicator_notes_set.all()[0]
		
		writer.writerow([res[i].id, c, res[i].Quality, d, res[i].PBSB, res[i].ID_WB_Category, res[i].ID_Indicator_Type, res[i].ID_Indicator_Country, res[i].Source, a, e])

	return response

def download_indicators(request):
	ids_l = request.GET.get('ids')
	ids_l = map(int,ids_l.split(','))

	##################
	#  FINAL RESULT  #
	##################
	res = []
	for i in ids_l:
		res = res + [Indicator.objects.get(id = i)]

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="download.csv"'
	writer = csv.writer(response)
	writer.writerow(['(0) Index','(1) INDICATOR (n)','(2) INDICATOR QUALITY (3) (g, y, r)','(3) DATASETS AVAILABLE (Hyperlink)','(4) PBSB CATEGORY (5) ((1, 2, 3, 4, 5))','(5) WB CATEGORY (Theme)','(6) INDICATOR TYPE (2) (SbPb, Ops)','(7) INDICATOR COUNTRY (or region)(n=129 (incl 7 regions) (193)','(8) INDICATOR SOURCE','(9) COMMENTS (n)','(10) Notes'])
	for i in range(0, len(res)):
		if len(res[i].indicator_comments_set.all()) == 0:
			a = 'n/a'
		else:
			a = res[i].indicator_comments_set.all()[0]
		if len(res[i].indicator_notes_set.all()) == 0:
			b = 'n/a'
		else:
			b = res[i].indicator_notes_set.all()[0]
		if res[i].Description == None:
			c = 'n/a'
		else:
			c = res[i].Description
		if res[i].DataSets_Availables == None:
			d = 'n/a'
		else:
			d = res[i].DataSets_Availables
		if len(res[i].indicator_notes_set.all()) == 0:
			e = 'n/a'
		else:
			e = res[i].indicator_notes_set.all()[0]
		
		writer.writerow([res[i].id, c, res[i].Quality, d, res[i].PBSB, res[i].ID_WB_Category, res[i].ID_Indicator_Type, res[i].ID_Indicator_Country, res[i].Source, a, e])

	return response

def rest_pbsb(request):
	pbsb_c = PBSB_Category.objects.all().distinct()
	data = serializers.serialize("json", pbsb_c)
	return HttpResponse(data, content_type="application/json")

def rest_categories(request):
	wb_c = WB_Category.objects.all().distinct().values('Theme').order_by('Theme')
	wb_c = [{'Theme':str(x['Theme'])} for x in wb_c]
	data = simplejson.dumps(wb_c)
	return HttpResponse(data, content_type="application/json")