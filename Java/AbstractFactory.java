public class Client{
    public static void main(String[] args) {
        ComputerFactory computerFactory = new ComputerFactory();
        computerFactory.createComputer("LG");
    }
}

public class LGKeyboard implements Keyboard{
    public LGKeyboard()
    {
        System.out.println("LG 키보드 생성");
    }
}

public class SamsungKeyboard implements Keyboard{
    public SamsungKeyboard(){
        System.err.println("Samsung 키보드 생성");
    }
}

public interface Keyboard{

}

public class KeyboardFactory{
    public Keyboard createKeyboard(String type){
        Keyboard keyboard = null;
        switch(type){
            case "LG":
            keyboard = new LGKeyboard();
            break;
            case "Samsung":
            keyboard = new SamsungKeyboard();
            break;
        }
        return keyboard;
    }
}

public class LGMouse implements Mouse{
    public LGMouse(){
        System.out.println("LG 마우스 생성");
    }
}

public class SamsungMouse implements Mouse{
    public SamsungMouse(){
        System.out.println("Samsung 마우스 생성");
    }
}

public interface Mouse{

}

public class MouseFactory{
    public Mouse createMouse(String type){
        Mouse mouse = null;
        switch(type){
            case "LG":
            mouse = new LGMouse();
            break;
            case "Samsung":
            mouse = new SamsungMouse();
            break;
        }
        return mouse;
    }
}

public class ComputerFactory{
    public void createComputer(String type){
        KeyboardFactory keyboardFactory = new KeyboardFactory();
        MouseFactory mouseFactory = new MouseFactory();

        keyboardFactory.createKeyboard(type);
        mouseFactory.createMouse(type);
        System.out.println("--" + type + " 컴퓨터 완성--");
    }
}

