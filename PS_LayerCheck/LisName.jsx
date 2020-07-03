// =======================================================
var idsetd = charIDToTypeID( "getd" );
    var desc7 = new ActionDescriptor();
    var idnull = charIDToTypeID( "null" );
        var ref3 = new ActionReference();
        var idLyr = charIDToTypeID( "Lyr " );
        var idOrdn = charIDToTypeID( "Ordn" );
        var idTrgt = charIDToTypeID( "Trgt" );
        ref3.putEnumerated( idLyr, idOrdn, idTrgt );
    desc7.putReference( idnull, ref3 );
    var idT = charIDToTypeID( "T   " );
        var desc8 = new ActionDescriptor();
        var idNm = charIDToTypeID( "Nm  " );
        desc8.putString( idNm, """222""" );
    var idLyr = charIDToTypeID( "Lyr " );
    desc7.putObject( idT, idLyr, desc8 );
var r=executeAction( idsetd, desc7, DialogModes.NO );
alert (r.getString(idNm))