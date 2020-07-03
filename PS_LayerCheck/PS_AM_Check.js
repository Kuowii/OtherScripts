var ChinesePhonetic=[
'a','ai','an','ang','ao',
'ba','bai','ban','bang','bao','bei','ben','beng','bi','bian','biao','bie','bin','bing','bo','bu',
'ca','cai','can','cang','cao','ce','cen','ceng','cha','chai','chan','chang','chao','che','chen','cheng','chi','chong','chou','chu','chua','chuai','chuan','chuang','chui','chun','chuo','ci','cong','cou','cu','cuan','cui','cun','cuo',
'da','dai','dan','dang','dao','de','dei','den','deng','di','dia','dian','diao','die','ding','diu','dong','dou','du','duan','dui','dun','duo',
'e','en','eng','er',
'fa','fan','fang','fei','fen','feng','fiao','fo','fou','fu',
'ga','gai','gan','gang','gao','ge','gei','gen','geng','gong','gou','gu','gua','guai','guan','guang','gui','gun','guo',
'ha','hai','han','hang','hao','he','hei','hen','heng','hong','hou','hu','hua','huai','huan','huang','hui','hun','huo',
'ji','jia','jian','jiang','jiao','jie','jin','jing','jiong','jiu','ju','juan','jue',
'ka','kai','kan','kang','kao','ke','ken','keng','kong','kou','ku','kua','kuai','kuan','kuang','kui','kun','kuo',
'la',
'lai',
'lan',
'lang',
'lao',
'le',
'lei',
'leng',
'li',
'lia',
'lian',
'liang',
'liao',
'lie',
'lin',
'ling',
'liu',
'lo',
'long',
'lou',
'lu',
'luan',
'lun',
'luo',
'lv',
'lve',
'ma',
'mai',
'man',
'mang',
'mao',
'me',
'mei',
'men',
'meng',
'mi',
'mian',
'miao',
'mie',
'min',
'ming',
'miu',
'mo',
'mou',
'mu',
'na',
'nai',
'nan',
'nang',
'nao',
'ne',
'nei',
'nen',
'neng',
'ni',
'nian',
'niang',
'niao',
'nie',
'nin',
'ning',
'niu',
'nong',
'nou',
'nu',
'nuan',
'nun',
'nuo',
'nv',
'nve',
'o',
'ou',
'pa',
'pai',
'pan',
'pang',
'pao',
'pei',
'pen',
'peng',
'pi',
'pian',
'piao',
'pie',
'pin',
'ping',
'po',
'pou',
'pu',
'qi',
'qia',
'qian',
'qiang',
'qiao',
'qie',
'qin',
'qing',
'qiong',
'qiu',
'qu',
'quan','que','qun',
'ran','rang','rao','re','ren','reng','ri','rong','rou','ru','rua','ruan','rui','run','ruo',
'sa','sai','san','sang','sao','se','sen','seng','sha','shai','shan','shang','shao','she','shei','shen','sheng','shi','shou','shu','shua','shuai','shuan','shuang','shui','shun','shuo','si','song','sou','su','suan','sui','sun','suo',
'ta','tai','tan','tang','tao','te','tei','teng','ti','tian','tiao','tie','ting','tong','tou','tu','tuan','tui','tun','tuo',
'wa','wai','wan','wang','wei','wen','weng','wo','wu',
'xi','xia','xian','xiang','xiao','xie','xin','xing','xiong','xiu','xu','xuan','xue','xun',
'ya','yan','yang','yao','ye','yi','yin','ying','yo','yong','you','yu','yuan','yue','yun',
'za','zai','zan','zang','zao','ze','zei','zen','zeng','zha','zhai','zhan','zhang','zhao','zhe','zhei','zhen','zheng','zhi','zhong','zhou','zhu','zhua','zhuai','zhuan','zhuang','zhui','zhun','zhuo','zi','zong','zou','zu','zuan','zui','zun','zuo'
];

function Dictionary(){
    this.add = add;
    this.datastore = new Object();
    this.find = find;
    this.remove = remove;
    this.length = length;
    this.count = count;
    this.clear = clear;
    return this;
}

function add(key, value){
    this.datastore[key] = value;
}

function find(key){
    return this.datastore[key];
}

function remove(key){
    delete this.datastore[key];
}

function count(){
    var n = 0;
    for (var key in this.datastore) {
        ++n;
    }
    return n;
}
function clear(){
    for (var key in this.datastore) {
        delete this.datastore[key];
    }
}

var doc = app.activeDocument;
var name_result=new Array();
var set_result=new Array();
var pattern = /^[A-Za-z0-9]+$/;
var dic_color=new Object();

function GetLayerUserColor(l){
    doc.activeLayer=l;
    var idsetd = charIDToTypeID( "getd" );
    var desc19 = new ActionDescriptor();
    var idnull = charIDToTypeID( "null" );
        var ref4 = new ActionReference();
        var idLyr = charIDToTypeID( "Lyr " );
        var idOrdn = charIDToTypeID( "Ordn" );
        var idTrgt = charIDToTypeID( "Trgt" );
        ref4.putEnumerated( idLyr, idOrdn, idTrgt );
    desc19.putReference( idnull, ref4 );
    var idT = charIDToTypeID( "T   " );
        var desc20 = new ActionDescriptor();
        var idClr = charIDToTypeID( "Clr " );
        var idBl = charIDToTypeID( "Bl  " );
        desc20.putEnumerated( idClr, idClr, idBl );
    var idLyr = charIDToTypeID( "Lyr " );
    desc19.putObject( idT, idLyr, desc20 );
return executeAction( idsetd, desc19, DialogModes.NO ).getEnumerationValue(idClr);
    }

var rew=new Window('dialog','AM Check Result',undefined,{closeButton:true });
rew.lbName=rew.add('statictext',undefined,'Name is illegality')
rew.lsName=rew.add('ListBox',[0,0,250,200]);
rew.lbName=rew.add('statictext',undefined,'Color group is unmatch.')
rew.lsSet=rew.add('ListBox',[0,0,250,200]);
rew.lbChannel=rew.add('statictext',undefined,'');

var dlg = new Window('dialog', 'AM Project Check 1.0 by Wings',undefined,{closeButton:true });

dlg.txtLog=dlg.add('statictext',undefined,undefined,{multiline:true});
dlg.cbLayerName=dlg.add('checkbox',undefined,'LayerNameCheck');
dlg.cbSetName=dlg.add('checkbox',undefined,'LayerSetNameCheck');
dlg.cbGroup=dlg.add('checkbox',undefined,'LayerSetColorGroupCheck');
dlg.cbChannel=dlg.add('checkbox',undefined,'AlphaChannelCheck');
dlg.cbLayerName.alignment='left';
dlg.cbSetName.alignment='left';
dlg.cbGroup.alignment='left';
dlg.cbChannel.alignment='left';
dlg.btnCheck = dlg.add('button', [0,0,250,20], 'Check',{name:'OK'});
dlg.btnCheck.onClick = Check;
dlg.show();

function Log(log,isclean){
    if(isclean == undefined){isclean=true}
    if(isclean){
        dlg.txtLog.text=log;
        }else{
         dig.txtLog.text+=log;
            }
    }

function Test(){
     var str="armor";
    var b = NameIsVaild(str);
    alert(b);
    }

function LayerNameCheck(layer,index){
    if(!NameIsVaild (layer.name)){
        name_result.push(layer);  
        }
    }

function SetColorCheck(set,index){
    var idc=GetLayerUserColor(set);
    if(idc!=undefined&&idc!=1315925605){    
        var iddic=dic_color[idc];
        if(iddic!=undefined){
            if(iddic.name!=set.name/*&&set.parent==iddic.parent*/){
                set.unmatch=iddic.name;
                set_result.push(set);
                }
            }else{
                dic_color[idc]=set;
                }
        }
    }

function CheckChannel(d){
    return d.channels.length>=4;
    }

function getLayers(set)
{ 
            for(var i =0;i<set.artLayers.length;i++){               
                if(dlg.cbLayerName.value){LayerNameCheck(set.artLayers[i],i)};
            }
           for(var i =0;i<set.layerSets.length;i++){
               
               if(dlg.cbGroup.value){SetColorCheck(set.layerSets[i],i);}
               if(dlg.cbSetName.value){LayerNameCheck(set.layerSets[i],i);}    
               getLayers(set.layerSets[i]);
            }   
    }
    
    function Check() {
        //alert(GetLayerUserColor ());
        getLayers (doc);
        var bChannel =true;
         if(dlg.cbChannel.value){bChannel=CheckChannel(doc);}    
        if(name_result.length>0 || set_result.length>0 || !bChannel)
        {
            for(var i =0;i<name_result.length;i++){
                rew.lsName.add('item',name_result[i].name);
                }
            for(var i =0;i<set_result.length;i++){
                rew.lsSet.add('item',set_result[i].name+ ' diff from '+set_result[i].unmatch);
                }
            
            if(!bChannel){
                rew.lbChannel.text='There is no alpha channel.';
                }
            
            rew.show();
            }else{
                alert('All pass.');
                }
}



function StartsWith(p,s,index){
    if(index==undefined){index=0}
    
    if((index+s.length)>p.length){return false}
    
    for(var i=0;i< s.length;i++){
        if(p[i+index]!=s[i]){
            return false;
            }
        }
    return true;
    }

function GetMax(arr){
    var len=arr[0].length;
    }

function NameIsVaild(name){
    
    if(!pattern.test(name)){return false;}
    
    var low=name.toLowerCase().replace(" ","").replace("_","").replace("-","");

        var r=false;
        var StartWithCPLen=0;
        var index=0;
        do{
            StartWithCPLen=0;
            var ls_match=[];
                for(var i=0;i< ChinesePhonetic.length;i++){
                   if(StartsWith(low,ChinesePhonetic[i],index)){
                       ls_match.push(ChinesePhonetic[i]);
                       }
                   }               
               
               if(ls_match.length>0){
                   index+=ls_match.sort(function(a,b){return b.length-a.length})[0].length;
                   }else
               {
                   r=true;
                   }
               
               }while(!r&&index<low.length);    
    return r;
    }

