import maya.cmds as cmds

class BSKeyData:
    def __init__(self,name):
        self.name=name;
        self.KeyValues=[];
    def addKey(self,kv):
        self.KeyValues.append(kv);

class BSControlData:
    def __init__(self,name):
        self.name=name;
        self.bsBase=[];
        self.bsIndex=[];
    def addControl(self,b,i):
        self.bsBase.append(b);
        self.bsIndex.append(i);
    def setWeight(self,v):
        i=0;
        for b in self.bsBase:
            cmds.blendShape( b, e=1, w = (self.bsIndex[i],v) );
            i = i+1;
    def setKeyFrame(self,kf,v):
        i=0;
        for b in self.bsBase:
            cmds.setKeyframe('{0}.w[{1}]'.format(b,self.bsIndex[i]),t=kf,v=v);
            i = i+1;
        
def getAllBSControl():
    r={};
    ns = cmds.ls(typ="blendShape");
    for n in ns:
        ws = cmds.listAttr(f'{n}.w',m=1);
        for i in range(len(ws)):
            bn = ws[i]
            if not bn in r:
                r.setdefault(bn,BSControlData(bn));
            r[bn].addControl(n,i);
    return r;

def loadBSFromCSV(fp):
    with open(fp, 'r', encoding='utf-8') as f:lines=f.readlines();
    bss = [];
    for key in lines[0].split(","):
        #print(key);
        bsd = BSKeyData(key.lower());
        bss.append(bsd);
    for line in lines[1:]:
        kbs = line.split(",");
        index = 2;
        for kb in kbs[2:]:
            bss[index].addKey(kb);
            index = index+1;
    #print(bss[3].KeyValues);
    return bss;
        
def main():
    fp=cmds.fileDialog2(fileFilter="*.csv",caption="Select Facial Animation Data",fm=1)[0];
    bss = loadBSFromCSV(fp);
    con = getAllBSControl();
    
    for bs in bss:
        if bs.name in con:
            for i in  range(len(bs.KeyValues)):
                con[bs.name].setKeyFrame(i,float(bs.KeyValues[i]));
                
def main2():
    fp=cmds.fileDialog2(fileFilter="*.csv",caption="Select Facial Animation Data",fm=1)[0];
    bss = maya.utils.executeInMainThreadWithResult(loadBSFromCSV,fp );
    con = maya.utils.executeInMainThreadWithResult( getAllBSControl );
        
    keyCount = len(bss[2].KeyValues);
    dataCount = len(bss);
    
    cmds.playbackOptions(max=keyCount)
    print(f'Get {dataCount} * {keyCount} data.');
    
    progressWin = cmds.window('Wings BS Loader')
    cmds.rowLayout(numberOfColumns=2)
    progressControl = cmds.progressBar(width=300)
    cmds.button( label='Cancel', command='cmds.progressBar(progressControl, edit=1, isCancelled=1)' )
    cmds.showWindow( progressWin )
    cmds.progressBar( progressControl,
                                edit=True,
                                beginProgress=True,
                                isInterruptable=True,
                                status='Loading BlendShape...',
                                maxValue=keyCount*dataCount
                                )  
    for bs in bss:
        if cmds.progressBar(progressControl, query=True, isCancelled=True ):
            break;
        if bs.name in con:
            for i in  range(len(bs.KeyValues)):
                cmds.progressBar(progressControl, edit=True, step=1)          
                con[bs.name].setKeyFrame(i,float(bs.KeyValues[i]));
        else:
            cmds.progressBar(progressControl, edit=True, step=keyCount)
                            
    print('Finish!')
    cmds.progressBar(progressControl, edit=True, endProgress=True)
    try:
        cmds.deleteUI(progressWin);
    except:
        print(f'Error:');
    cmds.confirmDialog( title='Wings BS Loader', message='Load Compelete!');
    
main2(); 