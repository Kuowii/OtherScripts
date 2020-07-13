fn ShowOpenEdge i=(
	clearselection();
	select i.obj
	modPanel.setCurrentObject i.obj.baseObject
	subobjectLevel=2
	if classof i.obj == editable_poly or classof i.obj==PolyMeshObject then(
		local edges = polyOp.getEdgesUsingVert i.obj i.data[6]
		i.obj.selectedEdges=edges
	)else if classof i.obj == editable_mesh then(
		i.obj.selectedEdges=(i.data[6] as bitarray)
	)else(
		format "% is % ,can not do ShowOpenEdge\n" i.obj.name (classof i.obj)
		return 0;
	)
)

fn ShowOverlapFaces i=(
	clearselection();
	select i.obj
	if classof i.obj == editable_poly then(
		subobjectLevel=4
	)else if classof i.obj == editable_mesh then(
		subobjectLevel=3
	)else(
		format "% is % ,can not do ShowOverlapFaces\n" i.obj.name (classof i.obj)
		return 0;
	)
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
	modPanel.setCurrentObject i.obj.baseObject
	if classof i.obj == editable_poly or classof i.obj==PolyMeshObject then(
		subobjectLevel=4;
	)else if classof i.obj == editable_mesh then(
		subobjectLevel=3;
	)else(
		format "% is % ,can not do ShowNoSmoothGroupFace\n" i.obj.name (classof i.obj)
		return 0;
	)
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