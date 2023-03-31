// Dr.Gerg's Battery Box
// OpenSCAD definition file
// https://www.drgerg.com
// OpenSCAD Cheatsheet http://www.openscad.org/cheatsheet/index.html
//
// PARAMETER DEFINITIONS// PARAMETER DEFINITIONS
// 
// 60x60x60

use <LilWeatherPi_Fan_Polyhedron_cap.scad>

topPoints = [
    [28,28,-1],      //0
    [28,-28,-1],     //1
    [-28,-28,-1],    //2
    [-28,28,-1],     //3
    [0,0,56]];       //4  TDC

lowPoints = [
    [26,26,-1],      //0
    [26,-26,-1],     //1
    [-26,-26,-1],    //2
    [-26,26,-1],     //3
    [0,0,54]];       //4  TDC

topFaces = [
    [0,1,4],
    [1,2,4],
    [2,3,4],
    [3,0,4],
    [2,1,0],[0,3,2]];


module pyramid(){
    difference(){
    polyhedron(topPoints,topFaces);
    polyhedron(lowPoints,topFaces);
    }
}
module screw(){
    translate([16,16,-23])
    cylinder(h=20,r=1.5,center=true);
}
module screws(){
    screw();
    rotate(90)
    screw();
    rotate(180)
    screw();
    rotate(270)
    screw();
}


$fn=128;

// chimney
module chimney(){
    translate([0,0,-15.5])
    difference(){
        difference(){
            difference(){
                cube([44,44,30], center=true);
                cylinder(d=37.6,h=64,center=true);
            }
        }
    }
    // Screen holder
    difference(){
        translate([0,0,-2.5])
        union(){
        rotate([0,0,45])
        cube([80,4,4], center=true);
        rotate([0,0,135])
        cube([80,4,4], center=true);
        }
        cylinder(d=37.6,h=64,center=true);
    }

    translate([0,0,-2.5])
    difference(){
        cube([60,60,4], center=true);
        translate([0,0,.5])
        cube([56,56,6], center=true);
    }
screws();
}


chimney();
// #cap();
