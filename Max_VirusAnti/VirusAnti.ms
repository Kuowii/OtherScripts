fn selectFolder = (
    local folderPath = getSavePath caption:"选择包含 .max 文件的文件夹"
    if folderPath != undefined then folderPath else ""
)

fn getMaxFilesRecursive folder = (
    local maxFiles = #()
	local netDi = dotNetObject "System.IO.DirectoryInfo" folder
	local netFies = netDi.GetFiles "*.max" ((dotNetClass "System.IO.SearchOption").AllDirectories)
    
    for fi in netFies do (
        append maxFiles fi.FullName
    )
    maxFiles
)

fn notifyPython message = (
    --local pyFile = (getDir #temp) + "\\maxscript_command.txt"
	local pyFileInfo = dotNetObject "System.IO.FileInfo" (getSourceFileName())
	local dir = pyFileInfo.Directory.FullName
	local pyFile = dir + "\\maxscript_command.txt"
	print pyFile
    local f = openFile pyFile mode:"wt"
    if f != undefined then (
        format "%\n" message to:f
        close f
    )
)

fn captureViewportScreenshot savePath = (
    local cap = gw.getViewportDib()
    if cap != undefined then (
		cap.filename = savePath
		save cap
    )
)

fn processMaxFiles maxFiles outputDir = (
    for f in maxFiles do (
        try (
            notifyPython ("OPEN:" + f)
            loadMaxFile f useFileUnits:true quiet:false
            --local fileName = getFilenameFile f
            --local screenshotPath = outputDir + "\\" + fileName + ".png"
            --captureViewportScreenshot screenshotPath
            --print ("Saved screenshot: " + screenshotPath)
            sleep 5
        ) catch (
            print ("Failed to process file: " + f)
        )
    )
)

fn main = (
	local rootFolder = selectFolder()
	if rootFolder != "" then (
		--local outputDir = rootFolder + "\\Screenshots"
		local outputDir="D:\\Temp\\Screenshots"
		makeDir outputDir
		local maxFiles = getMaxFilesRecursive rootFolder
		print maxFiles
		if maxFiles.count > 0 then (
			processMaxFiles maxFiles outputDir
			messagebox "所有文件已处理完成!" title:"完成"
		) else (
			messagebox "未找到 .max 文件!" title:"错误"
		)
	) else (
		messagebox "未选择文件夹!" title:"错误"
	)
)
main()