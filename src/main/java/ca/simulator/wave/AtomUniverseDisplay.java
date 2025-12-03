package ca.simulator.wave;

import javafx.scene.control.Button;
import javafx.scene.layout.GridPane;
import javafx.scene.control.Label;

public class AtomUniverseDisplay extends GridPane{
    private AtomUniverseModel model;

    public AtomUniverseDisplay(AtomUniverseModel model){
        this.model = model;
        
        for(int i=0; i < model.getXdim(); i++){
            for(int j=0; j < model.getYdim(); j++){
                DisplayAtom da = new DisplayAtom();
                Button button = new Button(String.valueOf(da.display()) + "." + i +',' + j);
                this.add(button, i, j);
                button.setOnAction(da);
            }
        }
        

    }
}
