fn mulmatrix mx v=(
	for i = 1 to 4 do
	(
		for j = 1 to 3 do
		(
			mx[i][j] = mx[i][j] * v
		)
	)
	return mx
)

Version = "MorphTargetTool 1.0 by Wings";

localPoints=#()
refSouceMesh=undefined
refVertexMatrices=#()

--获取当前pose姿态下各个点的位置，并把其在骨骼变换矩阵中的信息存储下来
--如果点没有被额外编辑，那么在进入骨骼变换矩阵后，其位置和BindedPose是一致的
--如果有编辑，那么把骨骼矩阵中的新位置通过BindPose矩阵逆运算，可以得到其在BindPose下的世界位置
fn getPointsPositionNow tmesh=(
	local points=#()
	local numVerts = tmesh.numVerts
	local skinMod = tmesh.modifiers[Skin]
	local pointWorldPos
	local mesh_type = classOf tmesh
	for v=1 to numVerts do(
		local localToWorldMatrix = getTransformMatrixWithWeights skinMod v
		if mesh_type == PolyMeshObject then(
			pointWorldPos = polyop.getVert tmesh v
		)else(
			pointWorldPos = meshop.getVert tmesh v
		)
		local localPoint =pointWorldPos * (Inverse localToWorldMatrix)
		--format "Point[%] Position : %\n" pointIndex pointWorldPos
		
		append points localPoint
	)
	return points
)

fn getPointMatricesWithBone tmesh=(
	local mss = #()
	local numVerts = tmesh.numVerts
	local skinMod = tmesh.modifiers[Skin]
	for v=1 to numVerts do(
		local localToWorldMatrix = getTransformMatrixWithWeights skinMod v
		append mss localToWorldMatrix
	)
	return mss 
)

fn getTransformMatrixWithWeights skinMod pointIndex =
(
    local weightCount=skinOps.GetVertexWeightCount skinMod pointIndex
	local finalMatrix = matrix3 0
	
	-- 遍历权重信息，获取每个骨骼的变换矩阵和权重
	for i = 1 to weightCount do
	(
		local boneIndex = skinOps.GetVertexWeightBoneID skinMod pointIndex i
		local boneWeight = skinOps.GetVertexWeight skinMod pointIndex i

		-- 获取骨骼的变换矩阵
		local tbone = skinOps.GetBoneNode skinMod boneIndex
		local boneTM = tbone.transform
		local mweight = mulmatrix boneTM boneWeight
		
		--format "% % \n" tbone.name tbone.transform
        
		finalMatrix += mweight
	)
    return finalMatrix
)

fn applyLocalPoint smesh tmesh points=(
	local numVerts = smesh.numVerts
	select smesh
	local mats= getPointMatricesWithBone smesh
	local mesh_type = classOf tmesh		
	for v=1 to numVerts do(
		local new_point=points[v]*mats[v]
		if mesh_type == PolyMeshObject or mesh_type==Editable_Poly then(
			polyop.setVert tmesh v new_point
		)else(
			meshop.setVert tmesh v new_point
		)
		
	)
)

rollout MorphTargetTool "MorphTargetTool"
(
	label lbVersion Version align:#right
	group "Operation"(
		button btnSave "SaveBindedPose"
		button btnLoad "Apply"
	)
	label lbDisplay ""
	on btnSave pressed do(
		print("Save Pose!")
		global localPoints,refSouceMesh
		localPoints=#()
		refSouceMesh = selection[1]
		localPoints =getPointsPositionNow refSouceMesh
	)
	on btnLoad pressed do(
		global localPoints,refSouceMesh
		applyLocalPoint refSouceMesh selection[1] localPoints
	)
)

try(
	closeRolloutFloater  MorphTargetToolFolater
)catch(print "MorphTargetToolFolater not create.")

MorphTargetToolFolater = newRolloutFloater Version 300 150
addRollout MorphTargetTool MorphTargetToolFolater rolledUp:false

