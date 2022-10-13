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

fn netGetFileInfo filefull=(
	local netFile = dotNetObject  "System.IO.FileInfo" filefull
	return #(netFile.Name,netFile.Directory.FullName,(getFilenameFile filefull));
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

fn saveMaxAnimationTo maxFull xafFull =(
		loadMaxFile maxFull useFileUnits:true quiet:true
		local nodes = (for obj in objects 
			where (classof obj == BoneGeometry or classof obj ==  Dummy or obj == Biped_Object) 
			collect obj)
			
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

fn saveBipAnimationTo bipFull=(
	return biped.saveBipFile $Bip001.controller bipFull #saveSubAnimControllers
)

fn useXafAnimationFile maxFull xafFull=(
		loadMaxFile maxFull useFileUnits:true quiet:true
		local nodes = (for obj in objects 
			where (classof obj == BoneGeometry or classof obj ==  Dummy or obj == Biped_Object) 
			collect obj)
			
		LoadSaveAnimation.loadAnimation xafFull nodes insert:true insertTime:0
)

fn useBipAnimationFile bipFull=(
	biped.loadBipFile $Bip001.controller bipFull #loadSubAnimControllers
)

rollout BatchApplyAnimationMenu "Batch ApplyAnimation" (
	
	local sourceFiles = undefined
	local targetFiles = undefined
		
	label lbVer "Create by Wings"
	group "Source File" (
		button btnSelectSourceFiles "Select Source Files"
		label lbInfoSource ""
	)
	group "Target File" (
		button btnSelectTargetFiles "Select Target Files"
		label lbInfoTarget ""
	)
	
	group "Process" (
		button btnMerge "Apply"
		checkbox isAutoDeleteTempXAF "Delete temp file" checked:true
	)
	
	fn BatchMainProcess sf tf=(
		
		if sf == undefined or tf == undefined then return 0
		
		for sourceFile in sf do(
			local info = netGetFileInfo sourceFile
			local nfp = stringstream ""
			format "%/Temp_%.xaf" info[2] info[3] to:nfp
			local xafFull = nfp as string
			
			local stBipfull = stringstream ""
			format "%/Temp_%.bip" info[2] info[3] to:stBipfull
			local bipFull = stBipfull as string
			
			local isUseBip = saveBipAnimationTo bipFull
			if not isUseBip then (
				print "Save Bip faild!"
				print bipFull
			)
			saveMaxAnimationTo sourceFile xafFull
			for targetFile in tf do(
				useXafAnimationFile targetFile xafFull
				if isUseBip then useBipAnimationFile bipFull
				local infoTarget = netGetFileInfo targetFile
				local nfp2 = stringstream ""
				format "%/%_%.max" infoTarget[2] infoTarget[3] info[3] to:nfp2
				saveMaxFile (nfp2 as string) useNewFile:true quiet:true
			)
			
			if isAutoDeleteTempXAF.checked do (
				deleteFile xafFull
				deleteFile bipFull
			)
		)
		
		messageBox "Compelete!"
	)
	
	on btnSelectSourceFiles pressed do (
		sourceFiles = openfiledlg "Select Source Files" "Max Files (*.max)|*.max|All Files (*.*)|*.*"
		if sourceFiles!=undefined then (
			local fc = sourceFiles.count;
			if(fc>1) then lbInfoSource.text=((fc as string) + " files." )
			else lbInfoSource.text= sourceFiles[1]
		)
	)
	
	on btnSelectTargetFiles pressed do (
		targetFiles = openfiledlg "Select Target Files" "FBX Files (*.max)|*.max|All Files (*.*)|*.*"
		if targetFiles!=undefined then (
			local fc = targetFiles.count;
			if(fc>1) then lbInfoTarget.text=((fc as string) + " files." )
			else lbInfoTarget.text= targetFiles[1]
		)
	)
	
	
	
	on btnMerge pressed do (
		BatchMainProcess sourceFiles targetFiles
	)
)

if BatchApplyAnimationMenu_Floater != undefined then CloseRolloutFloater BatchApplyAnimationMenu_Floater
global BatchApplyAnimationMenu_Floater = newRolloutFloater "" 500 300 
addRollout BatchApplyAnimationMenu BatchApplyAnimationMenu_Floater