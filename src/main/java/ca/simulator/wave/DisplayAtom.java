package ca.simulator.wave;

import java.lang.reflect.Array;

public class DisplayAtom implements Atom {
    double Energy;
    int direction;
    Atom[] NearAtoms = new Atom[8];

    public DisplayAtom (Atom[] nearByAtoms){
        Energy = 0;
        int counter = 0;
        for(Atom cAtom: nearByAtoms){
            NearAtoms[counter] = cAtom;
            counter ++;
        }
    }
    public void receive(int energy, int direction){
        this.Energy = energy;
        this.direction = direction;

    }
    public double display(){
        return this.Energy;
    }
    public void disperse(){
        // Depending on directions value (we can decide on encoding later, leaning towards numbers 1-9 being a direction) this atom should .recieve 
        // the correct atoms))
        switch (this.direction){
            case (0):
            break;
            default:
            break;
        }
    } 
    
}
