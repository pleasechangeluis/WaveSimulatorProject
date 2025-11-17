package ca.simulator.wave;

public interface Atom {
    void receive(int energy, int direction);
    double display();
    void disperse();
}
