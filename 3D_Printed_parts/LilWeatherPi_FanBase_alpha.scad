// Dr.Gerg's Battery Box
// OpenSCAD definition file
// https://www.drgerg.com
// OpenSCAD Cheatsheet http://www.openscad.org/cheatsheet/index.html
//
// PARAMETER DEFINITIONS// PARAMETER DEFINITIONS
// 
use <LilWeatherPi_Fan.scad>
use <LilWeatherPi_Fan_Polyhedron_cap.scad>
use <LilWeatherPi_Fan_Polyhedron_cap_chimney_final.scad>
wall = 2;  // how thick do you want the wall to be?
cornerDia = 11.2684; // The diameter of the filet on the back of the box.
totLength = 52; // Total length (y) of assembly.
totWidth = 54;  // Total width (x) of assembly.
filletAdd = 5.6342; // Added to cover curved edge on back of box.
baseHt = 4; // Thickness of the base only.
fanx =14;
fany = -40;
fanz = 0;

//

// module screw(){
//     translate([16,16,-23])
//     cylinder(h=20,r=1.5,center=true);
// }
// module screws(){
//     screw();
//     rotate(90)
//     screw();
//     rotate(180)
//     screw();
//     rotate(270)
//     screw();
// }

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
        translate([fanx,fany,4])
        union(){
            // screws();
            fanThroat();
        }
    }
}

module hollow(){
            translate([wall,-totLength+2*wall,0])
            cube([(totWidth-2*wall)+(cornerDia/2-wall),totLength-2*wall,8.2]);
            translate([fanx,fany,4])
            union(){
            fanThroat();
            translate([0,0,10])
            screws();
            translate([0,0,20])
            fanThroat();
            translate([0,0,4])
            fanFrame();
        }
}

module fanshroud(){
    difference(){
        translate([-1,-(totLength-2),4])
        cube([totWidth+filletAdd,totLength,21]);
        union(){
        hollow();
        translate([30,-24,55.5])
        screws();
        }
    translate([fanx,fany,8])
    fanbody();
    }
}


module fanbase(){
    difference(){
    baseAssy();
    translate([fanx,fany,8])
    translate([0,0,10])
    fanscrews();
    }
}


translate([30,-24,55.5])
union(){
#chimney();
#cap();
}

fanshroud();

// fanbase();