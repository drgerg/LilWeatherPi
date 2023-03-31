// Dr.Gerg's Battery Box
// OpenSCAD definition file
// https://www.drgerg.com
// OpenSCAD Cheatsheet http://www.openscad.org/cheatsheet/index.html
//
// PARAMETER DEFINITIONS// PARAMETER DEFINITIONS
// 
// 60x60x60


topPoints = [
    [30,30,0],      //0
    [30,-30,0],     //1
    [-30,-30,0],    //2
    [-30,30,0],     //3
    [0,0,60]];       //4  TDC

lowPoints = [
    [28,28,-1],      //0
    [28,-28,-1],     //1
    [-28,-28,-1],    //2
    [-28,28,-1],     //3
    [0,0,56]];       //4  TDC

topFaces = [
    [0,1,4],
    [1,2,4],
    [2,3,4],
    [3,0,4],
    [2,1,0],[0,3,2]];


module cap(){
    difference(){
    polyhedron(topPoints,topFaces);
    polyhedron(lowPoints,topFaces);
    }
}

cap();