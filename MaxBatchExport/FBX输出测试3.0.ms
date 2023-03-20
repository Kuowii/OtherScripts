fn openfiledlg title fil mul:true=(
	theDialog = dotNetObject  "System.Windows.Forms.OpenFileDialog"
	theDialog.title = title 
	theDialog.Multiselect = mul
	theDialog.Filter = fil 
	theDialog.FilterIndex = 1
	result = theDialog.showDialog()
if result.Equals result.OK then(
theFilenames = theDialog.fileNames
	if mul then return theFilenames else return  theFilenames[1]
)else (
	return undefined
)

)

fn FBX = 
(   
	a = maxFileName
	d = a.count
	f = d-4
    c = substring a 1 f    
	b = maxFilePath
    FileName = (b as string)+"\\"+(c as string)+".FBX"
    exportfile FileName #noprompt                       
	)
	
fn SFBX = 
(   
	a = maxFileName
	d = a.count
	f = d-4 
    c = substring a 1 f
	b = maxFilePath
    FileName = (b as string)+"\\"+(c as string)+".FBX"
    exportfile FileName #noprompt selectedOnly:true
	)	



try (destroyDialog Export)catch()

rollout Export "FBX导出（测试）"
(
	
				
	group "FBX"
	    (
			checkbox Animation "动画" tooltip:"Animation" pos:[10,20]  checked:False 
		    checkbox BakeAnimation "烘培" tooltip:"BakeAnimation" pos:[10,40]  checked:False
		    checkbox shape "变形" tooltip:"Morphs" pos:[10,60] checked:False
			checkbox Skin "蒙皮" tooltip:"Skin" pos:[10,80]  checked:False
			checkbox UseSceneName "场景名" tooltip:"UseSceneName" pos:[10,100]  checked:False
			
		    checkbox SmoothingGroups "平滑组" tooltip:"SmoothingGroups" pos:[85,20] checked:False
		    checkbox SmoothMeshExport "涡轮平滑" tooltip:"TurboSmooth" pos:[85,40] checked:true
			checkbox EmbedTextures "媒体" tooltip:"EmbedMedia" pos:[85,60] checked:False
			checkbox GeomAsBone "转化为骨骼" tooltip:"ConvertDeformingDummiesToBones" pos:[85,80] checked:true
			checkbox ColladaTriangulate "三角化" tooltip:"ColladaTriangulate" pos:[85,100] checked:False
			
		    checkbox Lights "灯光" tooltip:"Lights" pos:[170,20] checked:False
		    checkbox Cameras "摄像机" tooltip:"Cameras" pos:[170,40] checked:False
		    checkbox PreserveEdgeOrientation "边缘朝向" tooltip:"PreserveEdgeOrientation" pos:[170,60] checked:true
			checkbox AnimationClipClamp "动画选段" tooltip:"只导出当前动画轴设定的区域" pos:[170,80] checked:False

			Button btn1 "导出全部" tooltip:"ALL" width:80 height:35 pos:[30,120]
			Button btn2 "导出所选" tooltip:"selectedOnly" width:80 height:35 pos:[150,120]
			
			Button btn3 "批量导出全部" tooltip:"ALL" width:80 height:35 pos:[30,160]
			Button btn4 "批量导出所选" tooltip:"selectedOnly" width:80 height:35 pos:[150,160]
	        )
	
		
	fn FbxExport = 
		(
			FBXExporterSetParam "UseSceneName" UseSceneName.state
			FBXExporterSetParam "PreserveEdgeOrientation" PreserveEdgeOrientation.state
			FBXExporterSetParam "ColladaTriangulate" ColladaTriangulate.state
			FBXExporterSetParam "shape" shape.state
			FBXExporterSetParam "Skin" Skin.state
			FBXExporterSetParam "Animation" Animation.state
			FBXExporterSetParam "BakeAnimation"BakeAnimation.state
			FBXExporterSetParam "GeomAsBone" GeomAsBone.state
			FBXExporterSetParam "SmoothingGroups" SmoothingGroups.state
			FBXExporterSetParam "SmoothMeshExport" SmoothMeshExport.state
			FBXExporterSetParam "Lights" Lights.state
			FBXExporterSetParam "Cameras" Cameras.state
			FBXExporterSetParam "EmbedTextures" EmbedTextures.state
			
			if(AnimationClipClamp.state) then(
				local sn = getFilenameFile maxFileName
				FBXExporterSetParam "SplitAnimationIntoTakes" "-c"
				FBXExporterSetParam "SplitAnimationIntoTakes" sn animationRange.start animationRange.end
			)
			
		)
				
				
				
		
    
		on btn1 pressed  do
		    (		
				FbxExport()
				FBX()
		        )
		on btn1 rightclick do (shellLaunch (getFilenamePath maxFilePath) "")
				
		on btn2 pressed  do
		    (				
				FbxExport()
				SFBX()
		        )

		on btn3 pressed  do
		(	
		local sourceFiles = openfiledlg "Select Source Files" "Max Files (*.max)|*.max|All Files (*.*)|*.*"
		if sourceFiles!=undefined then (
			for sf in sourceFiles do(
				loadMaxFile sf useFileUnits:true quiet:true
				FbxExport()
				FBX()
			)
			messageBox "导出完成"
		)			
		)
		
		on btn4 pressed  do
		(	
		local sourceFiles = openfiledlg "Select Source Files" "Max Files (*.max)|*.max|All Files (*.*)|*.*"
		if sourceFiles!=undefined then (
			for sf in sourceFiles do(
				loadMaxFile sf useFileUnits:true quiet:true
				FbxExport()
				SFBX()
			)
			messageBox "导出完成"
		)			
		)

	    
	)
createDialog Export 260 210
