fn FnTest=(
	local obj=selection[1]
	local ff=obj.material.diffuseMap.filename;
	print ff
	local tts=meshop.getNumMaps obj
	print tts
)

fn FnTest2 ll=(
	print "Test2";
	local obj=selection[1]
	obj.selectedFaces=(ll as bitarray)
)

fn BaseCheckOnSelect i=(
		local obj = i.obj;
		if(obj.pos!=[0.0,0.0,0.0]) then
		(
			append i.result_type 1
		)
		if(isIdentity(obj.rotation) == false) then
		(
			append i.result_type 2
		)
		if(obj.scale!=[1.0,1.0,1.0]) then
		(
			append i.result_type 3
		)
)

fn UVOverlapCheck i=(	
	local isAddNew;
	local uvw=i.obj.modifiers[Unwrap_UVW];
	if uvw!=undefined then(
		isAddNew=false;
	)else(
		isAddNew=true;
		uvw=Unwrap_UVW()
		addmodifier i.obj uvw
	)
	subobjectLevel=3;
	uvw.selectOverlappedFaces();
	uvw.selectOverlappedFaces();
	local uvwface=uvw.getSelectedFaces();
	if uvwface != undefined then (	
	local faces = for f in uvwface collect f
	if faces.count>0 do (
		print (i.obj.name+ " overlap uv is "+(faces.count as string))			
		append i.result_type 4
		i.data[4]=faces
	)
	)
	--subobjectLevel=0
	if isAddNew do deletemodifier i.obj uvw
)

fn point3IsOutRange p=(
	return p.x>=0.0 and p.x<=1.0 and p.y>=0.0 and p.y<=1.0
)

fn UVRangeCheck i=(
	local l=#()
	local vertsCount,isPoly = false;
	--print("obj is "+(classof i.obj) as string);
	if classof i.obj == editable_poly then(
		vertsCount=polyop.getNumMapVerts i.obj 1
		isPoly=true;
		
	)else if classof i.obj == editable_mesh then(
		vertsCount=i.obj.numtverts;
		isPoly=false;
	)else(
		format "% is % ,can not do UVRangeCheck\n" i.obj.name (classof i.obj)
		return 0;
	)
	
	try(
			for v=1 to vertsCount do(
			local p = if isPoly then polyop.getMapVert i.obj 1 v else getTVert i.obj v
			if not point3IsOutRange(p) do(
				append l v
			)
		)
			if l.count>0 do(
				append i.result_type 5
				i.data[5]=l
			)
	)catch (
		--format "Error: % (% line:%)\n" (getCurrentException()) (getErrorSourceFileName()) (getErrorSourceFileLine())
		print(i.obj.name+" UVRangeCheck fail.")
	)
)

fn OpenEdgeCheck i=(
		try(
			local stl = STL_Check();
			local l=#(),isPoly=false;
			
			if classof i.obj == editable_poly then(
				isPoly=true;
			)else if classof i.obj == editable_mesh then(
				isPoly =false;
			)else(
				format "% is % ,can not do OpenEdgeCheck\n" i.obj.name (classof i.obj)
				return 0;
			)
			stl.Select_Faces =2;
			addmodifier i.obj stl
			stl.Check_Now=1
			local edges = for i in i.obj.selectedEdges collect i.index
			if edges.count>0 do(
				for f in edges do(
					--print f
					append l f
				)
				append i.result_type 6
				if isPoly then(
					i.data[6]=meshop.getVertsUsingEdge i.obj i.obj.selectedEdges
				)else(
					i.data[6]=edges
				)
			)
			deletemodifier i.obj stl
			
	)catch(
		print(i.obj.name+" OpenEdgeCheck fail.")
	)
	
)

fn SceneDataCheck data=(
	if units.SystemType!=data.data[1] then(
		print ("System unit is " + units.SystemType);
		print ("Check need set is " +data.data[1]);
		append data.result_type 101
	)
)

fn FacesCountCheck data=(
	clearselection();
	max select all;
	local count=0;
/* 	for i in selection do(
* 		faces=GetFaceSelection i 
* 		count+=faces.count;
* 	)
*/
	local fp=fileProperties.getItems "Mesh Totals"
	count=(filterString fp[2] " ")[2] as integer
	
	--print (fileProperties.getItems "Mesh Totals")[2]
	if count>data.data[1] then(
		append data.result_type 102
		local str = format "Overface set:% scene:% over:%" data.data[1] count (count-data.data[1])
		print str
	)
	clearselection();
)

fn SmoothGroupCheck i=(
	local count,getFSG;
	local l=#();
	
	if classof i.obj == editable_poly then(
		count=polyop.getNumFaces i.obj
		getFSG=polyop.getFaceSmoothGroup;
		
	)else if classof i.obj == editable_mesh then(
		count = i.obj.numfaces;
		getFSG=getFaceSmoothGroup;
	)else(
		format "% is % ,can not do SmoothGroupCheck\n" i.obj.name (classof i.obj)
		return 0;
	)
	
	for index=1 to count do(
		local sgv= getFSG i.obj index
		if( sgv ==0) then(
			append l index
		)
	)
	
	if(l.count>0) then(
		append i.result_type 7
		i.data[7]=l
	)
)


-- ???????
fn BonePoseCheck i=(
	local sk=i.obj.modifiers[Skin];
	if sk!=undefined then(
		local count=skinOps.GetNumberBones sk
		local lss=#();
		local r=#();
		local ori=currentTime
		print (i.obj.name + " have "+(count as string) +" bones.")
		local bonesNameList = for bn=1 to count collect (skinOps.GetBoneName sk bn 0)
		
		sliderTime=animationRange.start;
		for bn in bonesNameList do(
			local b=getnodebyname bn
			append lss b.transform
		)
		
		sliderTime=animationRange.end;
		for bn=1 to count do(
			local b=getnodebyname bonesNameList[bn]
			if b.transform!=lss[bn] do(
				append r b
			)
		)
		sliderTime=ori;
		
		if(r.count>0) do(
			append i.result_type 8
			i.data[8]=r
		)
		
	)else(
		print (i.obj.name + " is not a skin.")
	)
)

fn TextureSizeCheck i preset=(
	--local info = getBitmapInfo (i.obj.material.diffuseMap.filename);
	--local size=[info[3],info[4]];
	--print size;
	
	if(preset==undefined or preset.count<=0) do return 0;
	
	local arrmap=usedMaps(i.obj);
	local ls=#()
	for map in arrmap do(
		local info = getBitmapInfo (map);
		local isMatch = false;
		for p in preset do(
			if(p[1]==info[3] and p[2]==info[4]) do isMatch=true
		)
		if(not isMatch) do(
			append ls map
		)
	)
	
	if(ls.count>0) then(
		append i.result_type 9
		i.data[9]=ls
	)
)
 -- UV used area percent
fn UVAreaCheck i preset=(
	local isAddNew;
	local uvw=i.obj.modifiers[Unwrap_UVW];
	if uvw!=undefined then(
		isAddNew=false;
	)else(
		isAddNew=true;
		uvw=Unwrap_UVW()
		addmodifier i.obj uvw
	)
	subobjectLevel=3;
	max select all
	local uvwface=uvw.getSelectedFaces();
	if uvwface != undefined then (	
		local x,y,w,h,areauv,areag;
		uvw.getArea uvwface &x &y &w &h &areauv &areag
		format "x=%,y=%,w=%,h=%,uvw=%,geom=%\n" x y w h areauv areag
		local ss = (format ".2%" areauv)
		print ss
		if(areauv<preset) do(
			append i.result_type 10
			i.data[10]=areauv
		)
	)
	--subobjectLevel=0
	if isAddNew do deletemodifier i.obj uvw
	)