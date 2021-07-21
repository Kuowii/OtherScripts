struct aniFile(
	fbx="",
	xaf="",
	name="",
	frameCount=0,
	directory=""
)

fn openfiledlg title fil mul:true=(
	theDialog = dotNetObject  "System.Windows.Forms.OpenFileDialog"  --create a OpenFileDialog
	theDialog.title = title --set the title

-- This is the awesome bit! Activate the multi select :)
theDialog.Multiselect = mul --allow multiple files to be selected

-- Change this section as you would a normal max file open dialogue to filter the required image types
theDialog.Filter = fil --specify the filter
theDialog.FilterIndex = 1 --set the filter drop-down list to All Files
result = theDialog.showDialog() --display the dialog, get result into variable

result.ToString() --when closed, convert the result to string
result.Equals result.OK --returns TRUE if OK was pressed, FALSE otherwise
result.Equals result.Cancel --returns TRUE if Cancel was pressed, FALSE otherwise

-- And there you go, a nice need Array with all the filenames contained
theFilenames = theDialog.fileNames --the selected filenames will be returned as an array

if mul then return theFilenames else return  theFilenames[1]
)

fn netGetFileInfo filefull=(
	local netFile = dotNetObject  "System.IO.FileInfo" filefull
	return #(netFile.Name,netFile.Directory.FullName);
)

fn getSelectionArrary=(
	local sel=#()
	for i in selection do(
		append sel i
	)
	return sel
)

fn getObjAnimationLength objs=(
	if objs==undefined do return 0
	local tobjs = objs
	
	if (classOf tobjs != Array )do (
		tobjs = #()
		append tobjs objs
	)
	
	local len = tobjs.count
	
	local endtime = 0
	
	for i = 1 to len do
	(
		local obj = tobjs[i]
		
		sortKeys obj.controller
		
		local num_keys = numkeys obj.position.controller
		local keytiem = 0
		
		for j = 1 to num_keys do
		(
			key_time = getkeytime obj.position.controller j
			if key_time > endtime then endtime = key_time
		)
	)
	
	return endtime
)

fn saveFBXAnimationTo fbxFull xafFull =(
		importFile fbxFull #noPrompt using:FBXIMP
		local nodes = (for obj in objects where (classof obj == BoneGeometry or classof obj ==  Dummy) collect obj)
		local root = nodes[1];
		local userAttributes = #("")
		local userValues = #("")
		
		if xafFull == undefined do 
		(
			local temp = symbolicPaths.getPathValue "$temp"
			local tempFname = timeStamp() as string
			local nfp = stringstream ""
			format "%\\Temp_%.xaf" temp tempFname to:nfp
			nfp = nfp as string
			xafFull = nfp
		)
	
		LoadSaveAnimation.saveAnimation xafFull nodes userAttributes userValues
		
		return xafFull
)

fn logAllPath=(

	local count = symbolicPaths.numPaths()
	format "symbolicPaths.numPaths:%\n" count
	for i=1 to count do(
		local n = symbolicPaths.getPathName i
		local v = symbolicPaths.getPathValue i
		format "% : %\n" n v
	)
)

fn getFBXInfos filenames=(

	local infos=#()
	for f in filenames do(
		local fi = aniFile()
		local info = netGetFileInfo f
		fi.fbx = f
		fi.name = info[1]
		fi.directory = info[2]
		
		local nfp = stringstream ""
		format "%\\Temp_%.xaf" fi.directory fi.name to:nfp
		fi.xaf = nfp as string
		
		saveFBXAnimationTo fi.fbx fi.xaf
		
		append infos fi
	)
	
	return infos
)

fn mergeInOneScene infos fileFull=(

	--actionMan.executeAction 0 "16"  -- File: New Scene, Clear All ,it will ask for save
	resetMaxFile #noprompt
	
	importFile fileFull #noPrompt using:FBXIMP
	
	deleteKeys objects #allKeys
	
	local nodes = (for obj in objects where (classof obj == BoneGeometry or classof obj ==  Dummy) collect obj)
	
	for info in infos do(
		LoadSaveAnimation.loadAnimation info.xaf nodes insert:true
	)
		
	local frameCount = getObjAnimationLength nodes
	animationRange = interval animationRange.start frameCount
)

fn main=(
	--logAllPath();
	local temp = symbolicPaths.getPathValue "$temp"
	local filenames = openfiledlg "Select FBX Files" "FBX Files (*.fbx)|*.fbx|All Files (*.*)|*.*"
	local filerig = openfiledlg "Select Rig FBX Files" "FBX Files (*.fbx)|*.fbx|All Files (*.*)|*.*" mul:false
	local frameCount = 0
	
	local infos = getFBXInfos filenames
	
	--mergeInOneScene infos @"F:\UE_Projectes\UE4_VFX\Niagara_Dev\ArtResources\Idle_PreviewMesh.fbx"
	mergeInOneScene infos filerig
)

main()

