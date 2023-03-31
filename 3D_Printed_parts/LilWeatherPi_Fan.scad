// Dr.Gerg's Lil WeatherPi Vent Fan
// OpenSCAD definition file
// https://www.drgerg.com
// OpenSCAD Cheatsheet http://www.openscad.org/cheatsheet/index.html
//
// PARAMETER DEFINITIONS// PARAMETER DEFINITIONS
// 
wall = 1;  // how thick do you want the wall to be?
cornerDia = 7.68; // The diameter of the screw holes for the two pole contacts.
totLength = 40; // Total length of assembly.
totWidth = 40;  // Total width of assembly.
baseHt = 10.3; // Thickness of the fan only.
throat = 37.6; // diameter of fan.
screwR = 1.5; // radius of screw hole.

//
//// MAIN BODY OF BUILD
// COMPONENT BODY DEFINITION
//
module fanscrews(){
    translate([0,0,-19])
    cylinder(h=baseHt+20,r=screwR);
    translate([totLength-cornerDia,0,-19])
    cylinder(h=baseHt+20,r=screwR);
    translate([0,totWidth-cornerDia,-19])
    cylinder(h=baseHt+20,r=screwR);
    translate([totLength-cornerDia,totWidth-cornerDia,-19])
    cylinder(h=baseHt+20,r=screwR);
}
$fn=64;
module fanThroat(){
    translate([totLength/2-(cornerDia/2),totWidth/2-(cornerDia/2),-1])
    cylinder(h=baseHt+10,d=throat);
}


module fanFrame(){
        minkowski(){
        cube([totLength-cornerDia,totWidth-cornerDia,baseHt/2]);
        cylinder(baseHt/2,d=cornerDia);
        }
}


module fanbody(){
    union(){
        difference(){
                difference(){
                minkowski(){
                    cube([totLength-cornerDia,totWidth-cornerDia,baseHt/2]);
                    cylinder(baseHt/2,d=cornerDia);
                    }
                fanThroat();
                }
            fanscrews();
        }
    }
}
fanbody();