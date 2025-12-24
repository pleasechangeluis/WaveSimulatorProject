package ca.simulator.wave;

public class Universe {
    private Atom[][] UniverseGrid;
    private int width, height;

    public Universe(int width, int height){
        this.width = width;
        this.height = height;
        this.UniverseGrid = new Atom[width][height];

        for (int i = 0; i < width; i++){
            for (int j = 0; j < height; j++){
                UniverseGrid[i][j] = new Atom();
                if (i == 0 || i == width - 1 ||
                     j == 0 || j == height - 1){
                    UniverseGrid[i][j].isWall = true;
                }
            }
        }
    }

    public Atom GetAtom(int x, int y){
        return UniverseGrid[x][y];
    }

    public void click(int x, int y, double energy){
        if (UniverseGrid[x][y].isWall) {
            return;
        }
        UniverseGrid[x][y].energy += energy;
    }
    public void update(){

        // Update what the next frames should be
        for (int x = 1; x < width - 1; x++){
            for (int y = 1; y < height - 1; y++){

                // The psudo code lol
                Atom a = UniverseGrid[x][y];
                if (a.isWall) {
                    continue;
                }

                double leftEnergy = UniverseGrid[x - 1][y].energy;
                double rightEnergy = UniverseGrid[x + 1][y].energy;
                double upEnergy = UniverseGrid[x][y - 1].energy;
                double downEnergy = UniverseGrid[x][y + 1].energy;

                // The thing
                double newEnergy = ((leftEnergy + rightEnergy + 
                    upEnergy + downEnergy) / 2 )- a.NewEnergy;
                newEnergy = newEnergy * a.damping;
                a.NewEnergy = newEnergy;
            }
        }

        // Apply them
        for (int x = 1; x < width - 1; x++){
            for (int y = 1; y < height - 1; y++){
                Atom a = UniverseGrid[x][y];

                double temp = a.NewEnergy;
                a.NewEnergy = a.energy;
                a.energy = temp;
                // a.energy = a.NewEnergy;
            }
        }
    }
}
