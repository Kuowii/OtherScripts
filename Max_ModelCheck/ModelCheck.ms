include "ModelCheck_ShowResult.ms"

struct CheckResultData(
	obj,
	data=#(),
	result_type=#()
	)
	
global rn=#();
global ro=#();
global curOpObj;
	
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
	if faces!=undefined do (
		faces = faces as array;
		print (i.obj.name+ " overlap uv is "+(faces.count as string))
		if faces.count>0 do (
			append i.result_type 4
			append i.data (faces as bitarray)
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
			if point3IsOutRange(p) do(
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

fn CheckStart t=(
	--messagebox ("Check start " + (t as string))
	rn=#()
	ro=#()
	local sel=#();
		for i in selection do(
			append sel i
		)
	
	clearSelection();
		for i in sel do(
			select i
			curOpObj=CheckResultData i
			if CheckSetting.cbBase.checked do BaseCheckOnSelect(curOpObj)	
			if CheckSetting.cbUVLap.checked do UVOverlapCheck(curOpObj)
			if CheckSetting.cbUVRange.checked do UVRangeCheck(curOpObj)
			if CheckSetting.cbOpenEdge.checked do OpenEdgeCheck(curOpObj)
			if(curOpObj.result_type.count>0) then
			(
				append rn i.name
				append ro curOpObj
			)
		)
	createdialog CheckResultPanel
	)

rollout CheckResultPanel "Result" width:800 height:500
(
	listbox robjs "Objects" width:200 height:30 across:2 items:rn
	listbox ops "Operations" width:500 height:30 offset:[-150,0]
	on robjs selected i do(
		local l=#()
		for t in ro[i].result_type do(
			case t of (
				1:(append l "Not at origin.")
				2:(append l "Not zero rotate.")
				3:(append l "Not one scale.")
				4:(append l "UV overlap.")
				5:(append l "UV over range.")
				6:(append l "Open edge")
			)
		)
		ops.items=l;
	)
	
	on ops selected i do(
		case ops.items[i] of(
			"Open edge":(ShowOpenEdge(ro[robjs.selection]))
		)
	)
	
)

rollout CheckSetting "Setting"
(
	group "Check Item"(
	checkbox cbBase "BaseCheck" checked:true across:3
	checkbox cbUVLap "UV Overlap" checked:false
	checkbox cbUVRange "UV Range" checked:false
	checkbox cbOpenEdge "Open Edge" checked:false across:3
	checkbox cbSceneData "Scene Data" checked:false 
	checkbox cbFaceCount "Face Count" checked:false
	checkbox cbTexSize "Texture Size" checked:false across:3
	checkbox cbSmooth "Smooth Group" checked:false
	label lb ""
	)
	group "Check Operation"(
	button btnCheckStart "Check" across:2
	button btnTest "Test"
	button btnTest2 "Test2"
	)
	on btnCheckStart pressed do(
		CheckStart(666)
	)
	
	on btnTest pressed do (local ll=FnTest();FnTest2(ll))
	--on btnTest2 pressed do (FnTest2())
)

rollout BaseCheck "BaseCheck"
(
--slider happy "Happy" orient:#vertical across:5
--slider sad "Sad" orient:#vertical
--slider oo "OO" orient:#vertical
--slider ee "EE" orient:#vertical
	group "Setting"(
		)
	group "Result"(
		edittext r text:"No result." readOnly:true height:180 scrollbar:true
		)

)

MainRolloutFolater = newRolloutFloater "ModelCheck" 800 500
addRollout CheckSetting MainRolloutFolater rolledUp:false
addRollout BaseCheck MainRolloutFolater rolledUp:true
--addRollout test MainRolloutFolater


