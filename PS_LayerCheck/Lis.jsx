// =======================================================
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
    //alert("bl="+idBl+" clr="+idClr);
var a = executeAction( idsetd, desc19, DialogModes.NO );
alert(a.getEnumerationValue(idClr));
//2368-blue
//9431-yellow
//5606-None
