package ca.simulator.wave;
import javafx.animation.AnimationTimer;
import javafx.application.Application;
import javafx.scene.image.PixelWriter;
import javafx.scene.input.MouseEvent;
import javafx.scene.Scene;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.canvas.Canvas;
import javafx.scene.layout.StackPane;
import javafx.scene.paint.Color;
import javafx.stage.Stage;

public class Main extends Application {

    // Dimensions and zoom
    private static final int WIDTH = 400;  
    private static final int HEIGHT = 400; 
    private static final int SCALE = 2;    
    private Universe Universe;

    @Override
    public void start(Stage stage) {
        Universe = new Universe(WIDTH, HEIGHT);
        Canvas canvas = new Canvas(WIDTH * SCALE, HEIGHT * SCALE);
        GraphicsContext gc = canvas.getGraphicsContext2D();

        canvas.addEventHandler(MouseEvent.MOUSE_PRESSED, e -> createRipple(e));

        new AnimationTimer() {
            @Override
            public void handle(long now) {
                Universe.update();
                render(gc);
            }
        }.start();

        stage.setTitle("Wave Simulator");
        stage.setScene(new Scene(new StackPane(canvas), Color.BLACK));
        stage.show();
    }
    private void createRipple(MouseEvent e) {
        int x = (int)(e.getX() / SCALE);
        int y = (int)(e.getY() / SCALE);
        // magic number
        Universe.click(x, y, 1000);
    }

    private void render(GraphicsContext gc) {
        PixelWriter pw = gc.getPixelWriter();
        for (int x = 0; x < WIDTH; x++) {
            for (int y = 0; y < HEIGHT; y++) {
                Atom atom = Universe.GetAtom(x, y);
                if (atom.isWall) {
                    // Pixel thing
                    pw.setColor(x * SCALE, y * SCALE, Color.GRAY);
                    pw.setColor(x * SCALE + 1, y * SCALE, Color.GRAY);
                    pw.setColor(x * SCALE, y * SCALE + 1, Color.GRAY);
                    pw.setColor(x * SCALE + 1, y * SCALE + 1, Color.GRAY);
                    continue;
                }
                
                double energy = atom.energy;

                // Pixel thing that the vscode auto fill did.
                int colorValue = (int)Math.min(255, Math.abs(energy) * 5);
                Color color = Color.rgb(colorValue, colorValue, colorValue);

                for (int dx = 0; dx < SCALE; dx++) {
                    for (int dy = 0; dy < SCALE; dy++) {
                        pw.setColor(x * SCALE + dx, y * SCALE + dy, color);
                    }
                }
            }
        }
    }
    public static void main(String[] args) {
        launch(args);
    }
}
