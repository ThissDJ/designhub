function filenameWithSize(fn,size){
	var splitStr = fn.split(/\./g);
	var mapResult = splitStr.map(function(item,index,array){
		if(index === splitStr.length - 1){
			return (size === undefined?'':(size + '.' )) + item
		}else{
			return item
		}
	});
	return mapResult.join('.');
}