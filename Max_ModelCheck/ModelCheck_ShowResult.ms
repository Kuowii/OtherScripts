fn ShowOpenEdge i=(
	clearselection();
	select i.obj
	subobjectLevel=3
	try(
		i.obj.selectedFaces=(i.data[6] as bitarray)
	)catch(
		print(i.obj.name+" is not a mesh(ShowOpenEdge).")
	)
)

fn ShowOverlapFaces i=(
	clearselection();
	select i.obj
	subobjectLevel=3
	try(
		i.obj.selectedFaces=(i.data[4] as bitarray)
	)catch(
		print (i.obj.name + " is not a mesh(ShowOverlapFaces).")
	)
)

fn ShowUVOverRange i=(
	clearselection();
	select i.obj
	subobjectLevel=0
	local isAddNew;
	local uvw=i.obj.modifiers[Unwrap_UVW];
	if uvw!=undefined then(
		isAddNew=false;
	)else(
		isAddNew=true;
		uvw=Unwrap_UVW()
		uvw.name="ShowUVOverRange"
		addmodifier i.obj uvw
	)
	subobjectLevel=1;
	uvw.selectVertices (i.data[5] as bitarray) 
)

fn ShowNoSmoothGroupFace i =(
	clearselection();
	select i.obj
	subobjectLevel=3;
		try(
		i.obj.selectedFaces=(i.data[7] as bitarray)
	)catch(
		print (i.obj.name + " is not a mesh(ShowNoSmoothGroupFace).")
	)
)

fn ShowBonesPoseSEUnmatch i=(
	clearselection();
	subobjectLevel=0;
	for bn in i.data[8] do(
		selectmore bn
	)
)

fn ShowTextureSizeUnmatch i=(
	clearselection();
	subobjectLevel=0;
	select i.obj;
	local info="";
	for map in i.data[9] do(
		info=info+map+"\n";
	)
	Messagebox info;
)