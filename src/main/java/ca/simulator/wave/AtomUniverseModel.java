package ca.simulator.wave;

import javafx.scene.layout.GridPane;

public class AtomUniverseModel {
    private int xdim;
    private int ydim;

    public AtomUniverseModel(int x, int y){
        this.xdim = x;
        this.ydim = y;
    }

    public int getXdim(){
        return xdim;
    }
    public int getYdim(){
        return ydim;
    }
        
}
