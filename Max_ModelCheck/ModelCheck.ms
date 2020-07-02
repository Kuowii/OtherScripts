include "ModelCheck_ShowResult.ms"
include "ModelCheck_Check.ms"

struct CheckResultData(
	obj,
	data=#(),
	result_type=#()
	)
	
global rn=#();
global ro=#();
global curOpObj;

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
			if CheckSetting.cbSmooth.checked do SmoothGroupCheck(curOpObj)
			if(curOpObj.result_type.count>0) then
			(
				append rn i.name
				append ro curOpObj
			)
		)

		if CheckSetting.cbSceneData.checked do (
			curOpObj=CheckResultData()
			curOpObj.data[1]=SceneDataCheckSetting.SceneDataUnit.selected
			SceneDataCheck(curOpObj)
			if(curOpObj.result_type.count>0) then
			(
				append rn "Unit"
				append ro curOpObj
			)
		)
		
		if CheckSetting.cbFaceCount.checked do (
			curOpObj=CheckResultData()
			curOpObj.data[1]=FaceCountCheckSetting.spFaceCount.value
			FacesCountCheck(curOpObj)
			if(curOpObj.result_type.count>0) then
			(
				append rn "Faces Count"
				append ro curOpObj
			)
		)
		
		if ro.count>0 then(
			createdialog CheckResultPanel
		)else(
			Messagebox "ALL check pass!"
		)
	
	)

rollout CheckResultPanel "Result" width:800 height:500
(
	listbox robjs "Objects" width:200 height:30 across:2 items:rn
	listbox ops "Operations" width:500 height:30 offset:[-150,0]
	on robjs selected i do(
		subObjectLevel=0;
		if ro[i].obj!=undefined do select ro[i].obj
		local l=#()
		for t in ro[i].result_type do(
			case t of (
				1:(append l "Not at origin")
				2:(append l "Not zero rotate")
				3:(append l "Not one scale")
				4:(append l "UV overlap")
				5:(append l "UV over range")
				6:(append l "Open edge")
				7:(append l "Not full smooth group")
				101:(append l "Unit is not corresponding")
				102:(append l "Faces count over")
			)
		)
		ops.items=l;
	)
	
	on ops selected i do(
		case ops.items[i] of(
			"Open edge":(ShowOpenEdge(ro[robjs.selection]))
			"UV overlap":(ShowOverlapFaces(ro[robjs.selection]))
			"UV over range":(ShowUVOverRange(ro[robjs.selection]))
			"Not full smooth group":(ShowNoSmoothGroupFace(ro[robjs.selection]))
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
	
	on btnTest pressed do (FnTest())
	--on btnTest2 pressed do (FnTest2())
)

rollout BaseCheck "BaseCheck"
(
	group "Setting"(
		)
	group "Result"(
		edittext r text:"No result." readOnly:true height:180 scrollbar:true
		)

)

rollout SceneDataCheckSetting "SceneData"
(
	local UnitSets=#(
		#Inches,
		#Feet,
		#Miles,
		#Millimeters,
		#Centimeters,
		#Meters,
		#Kilometers 
	)
	dropdownlist SceneDataUnit "Unit" items:UnitSets selection:5
)

rollout FaceCountCheckSetting "FaceCount"
(
	spinner spFaceCount "Count" type:#integer scale:10 range:[1,1000000,2000]
	--spFaceCount.value = 2000;
)

MainRolloutFolater = newRolloutFloater "ModelCheck" 800 500
addRollout CheckSetting MainRolloutFolater rolledUp:false
addRollout BaseCheck MainRolloutFolater rolledUp:true
addRollout SceneDataCheckSetting MainRolloutFolater rolledUp:true
addRollout FaceCountCheckSetting MainRolloutFolater rolledUp:true
--addRollout test MainRolloutFolater


