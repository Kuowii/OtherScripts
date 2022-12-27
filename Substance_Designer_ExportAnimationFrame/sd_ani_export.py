import os
import glob
import sd
from sd.tools import export
from sd.api.sdvaluefloat import SDValueFloat
from sd.api.sdproperty import SDPropertyCategory

def main():
    input_value = 0;
    min_value = 0;
    max_value = 1;
    difference = max_value-min_value;
    frames = 30;
    step = difference/frames;
    
    ids=['age'];
    folder_path='D:\\SD_Animsets\\'
    file_name = 'SD_Anim_Frame'
    file_type='\*.png'
    
    sd_context = sd.getContext();
    sd_application = sd_context.getSDApplication();
    sd_ui_mgr=sd_application.getUIMgr();
    graph = sd_ui_mgr.getCurrentGraph();
    
    category = SDPropertyCategory.Input;
    #print(dir(graph));
    ls = [];
    for id in ids:
        pi = graph.getPropertyFromId(id,category);
        ls.append(pi);
        
        #param = graph.getInputParameter(id);
        #print(dir(param));

    for frame in range(frames):
        for label_property in ls:
            graph.setPropertyValue(label_property,SDValueFloat.sNew(input_value));
            export.exportSDGraphOutputs(graph,folder_path,'{0}_{1}.png'.format(file_name,str(frame)));
        input_value = round((input_value + step),5);

main();