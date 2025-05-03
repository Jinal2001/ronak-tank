import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class Calculator {

    private JFrame frame;
    private JTextField textField;
    private StringBuilder currentInput;
    private double result;
    private String operator;



    public Calculator() {
        frame = new JFrame("Simple Calculator");
        textField = new JTextField();
        currentInput = new StringBuilder();
        result = 0;
        operator = "";

        // Frame settings
        frame.setSize(400, 600);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setLayout(new BorderLayout());

        // Text Field setup
        textField.setEditable(false);
        textField.setFont(new Font("Arial", Font.PLAIN, 40));
        frame.add(textField, BorderLayout.NORTH);



        // Panel for buttons
        JPanel panel = new JPanel();
        panel.setLayout(new GridLayout(4, 4));

        // Buttons setup
        String[] buttons = {
            "7", "8", "9", "/",
            "4", "5", "6", "*",
            "1", "2", "3", "-",
            "0", ".", "=", "+"
        };

        for (String label : buttons) {
            JButton button = new JButton(label);
            button.setFont(new Font("Arial", Font.PLAIN, 30));
            button.addActionListener(new ButtonClickListener());
            panel.add(button);
        }

        // Add the panel with buttons to the frame
        frame.add(panel, BorderLayout.CENTER);
    }

    public void display() {
        frame.setVisible(true);
    }

    // Action listener for the buttons
    private class ButtonClickListener implements ActionListener {

        @Override
        public void actionPerformed(ActionEvent e) {
            String command = e.getActionCommand();

            if ("0123456789.".contains(command)) {
                // If the button is a number or dot, add it to current input
                currentInput.append(command);
                textField.setText(currentInput.toString());
            } else if (command.equals("=")) {
                // Perform the calculation and show the result
                calculateResult();
                textField.setText(String.valueOf(result));
                currentInput.setLength(0);
            } else {
                // If the button is an operator, set it
                if (currentInput.length() > 0) {
                    calculateResult();
                }
                operator = command;
                result = Double.parseDouble(currentInput.toString());
                currentInput.setLength(0); // Clear current input
            }
        }
    }

    // Perform calculation based on the operator
    private void calculateResult() {
        double currentNumber = currentInput.length() == 0 ? 0 : Double.parseDouble(currentInput.toString());

        switch (operator) {
            case "+":
                result += currentNumber;
                break;
            case "-":
                result -= currentNumber;
                break;
            case "*":
                result *= currentNumber;
                break;
            case "/":
                if (currentNumber != 0) {
                    result /= currentNumber;
                } else {
                    textField.setText("Error");
                    return;
                }
                break;
        }
        currentInput.setLength(0);  // Clear current input after calculation
    }

    // Main method to run the program
    public static void main(String[] args) {
        Calculator calculator = new Calculator();
        calculator.display();
    }
}
