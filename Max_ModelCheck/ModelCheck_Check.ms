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
	uvw.selectOverlappedFaces();
	local faces=uvw.getSelectedFaces();
	local l=#();
	if faces!=undefined do (
		local arrfaces = faces as array;
		print (i.obj.name+ " overlap uv is "+(arrfaces.count as string))
		if arrfaces.count>0 do (
			
			for f in faces do(
				append l f
			)
			
			append i.result_type 4
			append i.data l
		)
	)
	if isAddNew do deletemodifier i.obj uvw
)

fn point3IsOutRange p=(
	return p.x>=0 and p.x<=1 and p.y>=0 and p.y<=1
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
				append i.data l
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
			local faces=i.obj.selectedFaces
			if faces.count>0 do(
				for f in faces do(
					--print f
					append l f
				)
				append i.result_type 6
				append i.data l
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