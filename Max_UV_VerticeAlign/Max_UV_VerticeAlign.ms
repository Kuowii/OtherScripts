Version = "UV_VerticeAlign 1.0 by Wings";

struct CheckResultData(
	obj,
	data=#(),
	result_type=#()
	)

struct point2data(
	p,
	id,
	dis
	)

fn compareDis p1 p2=(
	return p1.dis >= p2.dis
)

fn point2GetNearPoint p arr offset=(
	local nl = #();		
	for ap in arr do(
		local dis = distance ap.p p.p
		if  dis <= offset then(
			ap.dis = dis
			append nl ap
		)
	);
	
	qsort nl compareDis
	
	return nl;
)

fn UVAlign i=(
	local isPoly = false;
	
	try(
		local vertsCount=polyop.getNumMapVerts i.obj 1
		isPoly = true;
	)catch(
		isPoly = false;
	)
	
	local isAddNew;
	local uvw=i.obj.modifiers[Unwrap_UVW];
	if uvw!=undefined then(
		isAddNew=true;
	)else(
		isAddNew=false;
	)
	subobjectLevel=1;
	
	local vs=uvw.getSelectedVertices();
	local l = #();
	if vs != undefined then (	
	for v in vs do(
		local p = if isPoly then polyop.getMapVert i.obj 1 v else getTVert i.obj v
		local pd = point2data p v
		append l pd
		)
	)
	
	local len = l.count
	format "get % points isPoly % offset % \n" len isPoly CheckSetting.spOff.value
		
	local opCount = 0;
	for index = 1 to len do(
		local p = l[1];
		deleteItem l 1
		local tr = point2GetNearPoint p l CheckSetting.spOff.value
		if tr.count > 0 then(
			if isAddNew then(
				uvw.SetVertexPosition 1 p.id tr[1].p
			)else(
				if isPoly then polyop.setMapVert i.obj 1 p.id tr[1].p else setTVert i.obj p.id tr[1].p
			)
			opCount=opCount+1;
		)
	)
	format "Count:% Op:%\n" len opCount
	messagebox("Align Over!\n Select count:"+(len as string)+"\n Align count:"+(opCount as string));
)


fn AlignStart =(
	--messagebox ("Align start ")
		local sel=#();
		for i in selection do(
			append sel i
			curOpObj=CheckResultData i
			UVAlign(curOpObj);
		)
)


rollout CheckSetting "Setting"
(
	label lbVersion Version align:#right
	group "Operation"(
	spinner spOff "Offset" type:#float scale:0.01 range:[0,1,0.01]
	button btnCheckStart "Align"
	)
	on btnCheckStart pressed do(
		AlignStart()
	)
)

try(
	closeRolloutFloater  MainRolloutFolater
)catch(print "MainRolloutFolater not create.")

MainRolloutFolater = newRolloutFloater Version 300 150
addRollout CheckSetting MainRolloutFolater rolledUp:false