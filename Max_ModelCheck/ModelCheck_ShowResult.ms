fn ShowOpenEdge i=(
	clearselection();
	select i.obj
	subobjectLevel=3
	try(
		i.obj.selectedFaces=(i.data[1] as bitarray)
	)catch(
		print(i.obj.name+" is not a mesh.")
	)
)


fn FnTest=(
	local obj=selection[1]
			local stl = STL_Check();
			local l=#();
			addmodifier obj stl
			stl.Check_Now=1
			local faces=obj.selectedFaces as bitarray
			if faces.count>0 do(
				for f in faces do(
					append l f
				)
			)
			deletemodifier obj stl
	return l;
)

fn FnTest2 ll=(
	print "Test2";
	local obj=selection[1]
	obj.selectedFaces=(ll as bitarray)
)