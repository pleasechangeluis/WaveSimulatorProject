package ca.simulator.wave;
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.StackPane;
import javafx.stage.Stage;
public class View {
    private final Stage stage;
    private final AtomUniverseModel atomUniverseModel;
    private final AtomUniverseDisplay atomUniverseDisplay;

    public View(AtomUniverseModel model, Stage stage){
        this.atomUniverseModel = model;
        this.stage = stage;
        this.atomUniverseDisplay = new AtomUniverseDisplay(this.atomUniverseModel);
        BorderPane root = new BorderPane();
        root.setCenter(this.atomUniverseDisplay);

        Scene scene = new Scene(root);
        stage.setScene(scene);
        stage.setTitle("WaveSim");
        stage.show();
    }

    public Stage getStage(){return this.stage;}
    public AtomUniverseModel getAtomUniverseModel(){return this.atomUniverseModel;}
    public AtomUniverseDisplay getAtomUniverseDisplay(){return this.atomUniverseDisplay;}
}
