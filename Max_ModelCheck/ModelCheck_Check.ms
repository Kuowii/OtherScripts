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
	local uvwface=uvw.getSelectedFaces();
	print uvwface;
	local faces = for f in uvwface collect f
	if faces.count>0 do (
		print (i.obj.name+ " overlap uv is "+(faces.count as string))			
		append i.result_type 4
		i.data[4]=faces
	)
	--subobjectLevel=0
	if isAddNew do deletemodifier i.obj uvw
)

fn point3IsOutRange p=(
	return p.x>=0.0 and p.x<=1.0 and p.y>=0.0 and p.y<=1.0
)

fn UVRangeCheck i=(
	try(
			local l=#()
			for v=1 to i.obj.numtverts do(
			local p = getTVert i.obj v
			if not point3IsOutRange(p) do(
				append l v
			)
		)
			if l.count>0 do(
				append i.result_type 5
				i.data[5]=l
			)
	)catch(
		print(i.obj.name+" is not a mesh.")
	)
)

fn OpenEdgeCheck i=(
		try(
			local stl = STL_Check();
			local l=#();
			addmodifier i.obj stl
			stl.Check_Now=1
			local faces = for i in i.obj.selectedFaces collect i.index
			if faces.count>0 do(
				for f in faces do(
					print f
					append l f
				)
				append i.result_type 6
				i.data[6]=faces
			)
			deletemodifier i.obj stl
			
	)catch(
		print(i.obj.name+" is not a mesh.")
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
	for i in selection do(
		if(i.Faces!=undefined)then(
			count+=i.Faces.count;
		)
	)
	--print (fileProperties.getItems "Mesh Totals")[2]
	if count>data.data[1] then(
		append data.result_type 102
		local str = format "Overface set:% scene:% over:%" data.data[1] count (count-data.data[1])
		print str
	)
	clearselection();
)

fn SmoothGroupCheck i=(
	local count;
	local l=#();
	try(
		count = i.obj.numfaces;
	)catch(
		print(i.obj.name+" is not a mesh.")
		return 0;
	)
	
	for index=1 to count do(
		local sgv=getFaceSmoothGroup i.obj index
		if( sgv ==0) then(
			append l index
		)
	)
	
	if(l.count>0) then(
		append i.result_type 7
		i.data[7]=l
	)
)