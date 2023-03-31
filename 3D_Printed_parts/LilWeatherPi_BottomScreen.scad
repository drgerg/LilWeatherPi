// Dr.Gerg's Battery Box
// OpenSCAD definition file
// https://www.drgerg.com
// OpenSCAD Cheatsheet http://www.openscad.org/cheatsheet/index.html
//
// PARAMETER DEFINITIONS// PARAMETER DEFINITIONS
// 
use <LilWeatherPi_Fan.scad>
wall = 2;  // how thick do you want the wall to be?
cornerDia = 11.2684; // The diameter of the filet on the back of the box.
totLength = 87; // Total length of assembly.
baseHt = 4; // Thickness of the base only.
// totWidth = 54;  // Total width of assembly.
totWidth = 33.1158;
filletAdd = 5.6342; // Added to cover curved edge on back of box.
fanx =16;
fany = -19;
fanz = 0;
// 34.75 altogether
//
//// MAIN BODY OF BUILD
// COMPONENT BODY DEFINITION
//

$fn=128;
module main(){
    difference(){
        translate([wall,-totLength+2*wall,0])
        cube([(totWidth-2*wall)+(cornerDia/2-wall),totLength-2*wall,baseHt*2]);
        union(){
            translate([0,-totLength+wall,-wall*2])
            cube([totWidth-2*wall,totLength,baseHt*2]);
            translate([cornerDia/2,+wall,0])
            intersection(){
                translate([0,-totLength,-wall])
                cube([totWidth-2*wall,totLength+2*wall,baseHt*2]);
                translate([totWidth-2*wall-cornerDia/2,+wall/2,-cornerDia/2+baseHt])
                rotate([90,0,0])
                cylinder(totLength,d=cornerDia,center=false);
            }
        }
    }
}
module baseAssy(){
    difference(){
        main();
        union(){
            translate([fanx-2,fany+2,fanz])
            #cylinder(h=20,d=21,center=true);
            translate([fanx+2,-64,fanz])
            #cylinder(h=20,d=21,center=true);
            }
    }


}

baseAssy();