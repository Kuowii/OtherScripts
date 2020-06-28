fn ShowOpenEdge i=(
	clearselection();
	select i.obj
	subobjectLevel=3
	try(
		i.obj.selectedFaces=(i.data[1] as bitarray)
	)catch(
		print(i.obj.name+" is not a mesh(ShowOpenEdge).")
	)
)

fn ShowOverlapFaces i=(
	clearselection();
	select i.obj
	subobjectLevel=3
	try(
		i.obj.selectedFaces=(i.data[1] as bitarray)
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
	uvw.selectVertices (i.data[1] as bitarray) 
)
