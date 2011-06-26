//	HYPE.documents["Subscribe"]

(function HYPE_DocumentLoader() {
	var resourcesFolderName = "Subscribe_Resources";
	var documentName = "Subscribe";
	var documentLoaderFilename = "subscribe_hype_generated_script.js";

	// find the URL for this script's absolute path and set as the resourceFolderName
	try {
		var scripts = document.getElementsByTagName('script');
		for(var i = 0; i < scripts.length; i++) {
			var scriptSrc = scripts[i].src;
			if(scriptSrc != null && scriptSrc.indexOf(documentLoaderFilename) != -1) {
				resourcesFolderName = scriptSrc.substr(0, scriptSrc.lastIndexOf("/"));
				break;
			}
		}
	} catch(err) {	}

	// load HYPE.js if it hasn't been loaded yet
	if(typeof HYPE == "undefined") {
		if(typeof window.HYPE_DocumentsToLoad == "undefined") {
			window.HYPE_DocumentsToLoad = new Array();
		}
		window.HYPE_DocumentsToLoad.push(HYPE_DocumentLoader);

		var headElement = document.getElementsByTagName('head')[0];
		var scriptElement = document.createElement('script');
		scriptElement.type= 'text/javascript';
		scriptElement.src = resourcesFolderName + '/' + 'HYPE.js';
		headElement.appendChild(scriptElement);
		return;
	}
	
	var attributeTransformerMapping = {"BorderRadiusTopLeft":"PixelValueTransformer","BackgroundColor":"ColorValueTransformer","BorderWidthBottom":"PixelValueTransformer","BoxShadowXOffset":"PixelValueTransformer","WordSpacing":"PixelValueTransformer","Opacity":"FractionalValueTransformer","BorderWidthRight":"PixelValueTransformer","BorderWidthTop":"PixelValueTransformer","BoxShadowColor":"ColorValueTransformer","BorderColorBottom":"ColorValueTransformer","FontSize":"PixelValueTransformer","BorderRadiusTopRight":"PixelValueTransformer","TextColor":"ColorValueTransformer","Rotate":"DegreeValueTransformer","Height":"PixelValueTransformer","BorderColorTop":"ColorValueTransformer","PaddingLeft":"PixelValueTransformer","Top":"PixelValueTransformer","BackgroundGradientStartColor":"ColorValueTransformer","TextShadowXOffset":"PixelValueTransformer","PaddingTop":"PixelValueTransformer","BackgroundGradientAngle":"DegreeValueTransformer","PaddingBottom":"PixelValueTransformer","PaddingRight":"PixelValueTransformer","BorderColorLeft":"ColorValueTransformer","Width":"PixelValueTransformer","TextShadowColor":"ColorValueTransformer","ReflectionOffset":"PixelValueTransformer","Left":"PixelValueTransformer","BorderRadiusBottomRight":"PixelValueTransformer","ReflectionDepth":"FractionalValueTransformer","BoxShadowYOffset":"PixelValueTransformer","BorderColorRight":"ColorValueTransformer","LineHeight":"PixelValueTransformer","BorderWidthLeft":"PixelValueTransformer","TextShadowBlurRadius":"PixelValueTransformer","TextShadowYOffset":"PixelValueTransformer","BorderRadiusBottomLeft":"PixelValueTransformer","BackgroundGradientEndColor":"ColorValueTransformer","BoxShadowBlurRadius":"PixelValueTransformer","LetterSpacing":"PixelValueTransformer"};

var scenes = [{"timelines":{"kTimelineDefaultIdentifier":{"framesPerSecond":30,"animations":[{"startValue":"0.000000","isRelative":true,"endValue":"1.000000","identifier":"Opacity","duration":2,"timingFunction":"easeinout","type":0,"oid":"823091C6-644B-40B7-8578-09D1A4F92124-763-000013D809E0E28F","startTime":0},{"startValue":"0.000000","isRelative":true,"endValue":"1.000000","identifier":"Opacity","duration":2,"timingFunction":"easeinout","type":0,"oid":"1722CDB0-EB60-4EC1-9B87-10D606F5A0C2-389-0000042A2BA5915A","startTime":0}],"identifier":"kTimelineDefaultIdentifier","name":"Main Timeline","duration":2}},"id":"1A28CFBC-EE5A-466C-9656-026FEEA6E3BD-389-0000041E539776D4","sceneIndex":0,"perspective":"600px","oid":"1A28CFBC-EE5A-466C-9656-026FEEA6E3BD-389-0000041E539776D4","initialValues":{"1722CDB0-EB60-4EC1-9B87-10D606F5A0C2-389-0000042A2BA5915A":{"TagName":"div","BorderColorBottom":"#A0A0A0","Opacity":"0.000000","BorderStyleRight":"None","BorderStyleBottom":"None","Top":"88px","BorderWidthRight":"0px","BorderStyleLeft":"None","BorderColorTop":"#A0A0A0","BorderColorLeft":"#A0A0A0","Position":"absolute","Height":"24px","Left":"278px","BorderColorRight":"#A0A0A0","InnerHTML":"<form>\n<input type=\"text\" name=\"email\">\n<input type=\"submit\">\n</form>","BorderStyleTop":"None","ZIndex":"1","Width":"301px","BorderWidthTop":"0px","Overflow":"visible","BorderWidthLeft":"0px","BorderWidthBottom":"0px"},"823091C6-644B-40B7-8578-09D1A4F92124-763-000013D809E0E28F":{"Position":"absolute","PaddingTop":"8px","WhiteSpaceCollapsing":"preserve","PaddingRight":"8px","Left":"148px","Display":"inline","Overflow":"visible","Opacity":"0.000000","ZIndex":"2","Top":"83px","PaddingLeft":"8px","TextColor":"#000000","TagName":"div","PaddingBottom":"8px","InnerHTML":"<font class=\"Apple-style-span\" color=\"#FFFFFF\">E-Mail Address</font>","FontSize":"16px","WordWrap":"break-word"}},"name":"Untitled Scene","backgroundColor":"#000000"}];

var javascriptMapping = {};


	
	var Custom = (function() {
	return {
	};
}());

	
	var hypeDoc = new HYPE();
	
	hypeDoc.attributeTransformerMapping = attributeTransformerMapping;
	hypeDoc.scenes = scenes;
	hypeDoc.javascriptMapping = javascriptMapping;
	hypeDoc.Custom = Custom;
	hypeDoc.currentSceneIndex = 0;
	hypeDoc.mainContentContainerID = "subscribe_hype_container";
	hypeDoc.resourcesFolderName = resourcesFolderName;
	hypeDoc.showHypeBuiltWatermark = 0;
	hypeDoc.showLoadingPage = false;
	hypeDoc.drawSceneBackgrounds = true;
	hypeDoc.documentName = documentName;

	HYPE.documents[documentName] = hypeDoc.API;

	hypeDoc.documentLoad(this.body);
}());

