package lib;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.Scanner;

public class test {
    
    public static void main(String[] args) throws IOException {
        String command = "java -jar E:\\Praca_magisterska\\n" + //
                "arrative_system\\lib\\sabre.jar -p E:\\Praca_magisterska\\n" + //
                        "arrative_system\\lib\\hotel2.txt -el 0 -v";
        ProcessBuilder pb = new ProcessBuilder(command).redirectErrorStream(true);
        Process process = pb.start();
        StringBuilder result = new StringBuilder(80);
        try (BufferedReader in = new BufferedReader(new InputStreamReader(process.getInputStream())))
        {
            while (true)
            {
                String line = in.readLine();
                if (line == null)
                    break;
                result.append(line).append("/n");
            }
        }
        System.out.println(result);
    }
}
