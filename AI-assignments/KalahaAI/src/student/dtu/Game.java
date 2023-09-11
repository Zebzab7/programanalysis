package student.dtu;

import java.util.Scanner;

import student.dtu.AI.Node;



public class Game {
	
	public static enum Player {
		PlayerOne(1),
		PlayerTwo(0);

		public final int side;

		private Player(int side) {
			this.side = side;
		}

	}
	
	private static short[][] Board = new short[2][7];
	private static boolean aiEnabled = false;
	private static boolean aiBenchmarkingEnabled = false;
	private static boolean finished = false;
	static Player player = Player.PlayerOne;

	public static void initGame() {
		// Inits Game Array
		for (int i = 0; i < 2; i++) {
			for (int j = 0; j < 6; j++) {
				Board[i][j] = 4;
			}
		}
		printGame();
	}

	public static void runGame() {
		initGame();
		enableAI();
		while (!finished) {
			//Change this boolean to aiEnabled && player == Player.PlayerOne
			//if you want the AI to be playerOne
			if(aiEnabled && player == Player.PlayerTwo) {
				aiTurn();
			}
			else if(aiBenchmarkingEnabled) {
				aiTurn();
			}
			else {
				playerTurn();
			}
			
		}
		printScores();
	}
	
	public static void aiTurn() {
		AI ai = new AI(player);
		System.out.println("AI is deciding on a move.");
		int move = ai.aiMove(new Node(Board, true, 0, false, null, (short)-1));
		System.out.println("AI chose move: " + move);
		boolean nextTurn = updateGame(move);
		if(!nextTurn) {
			player = player == Player.PlayerTwo ? Player.PlayerOne : Player.PlayerTwo;
		}
		checkGameState();
		printGame();
	}
	
	public static void enableAI() {
		System.out.println("Enable AI: y/n");
		Scanner sc = new Scanner(System.in);
		if(sc.next().equals("y")) {
			aiEnabled = true;
			System.out.println("Enable AI benchmarking (AI vs AI): y/n");
			if(sc.next().equals("y")) {
				aiBenchmarkingEnabled = true;
			}
		}
	}
	
	public static void playerTurn() {
		boolean hasTurn = true;
		while (hasTurn) {
			boolean hasChosen = false;

			// Selecting one of the 6 bowls
			while (!hasChosen) {
				System.out.println(player + " choose one of six bowls with the numbers 1-6");
				Scanner sc = new Scanner(System.in);
				String input = sc.nextLine();

				// Controls input
				if (!input.matches("[1-6]")) {
					System.out.println("Input is not a number between 1 and 6");
				} else {
					if (Board[player.side][Integer.parseInt(input)-1] != 0) {
						hasChosen = true;
						System.out.println("Right number chosen");
						hasTurn = updateGame(Integer.parseInt(input));
						checkGameState();	
					}
					else {
						System.out.println("Bowl is Empty choose nonempty bowl");
					}
				}
			}
			printGame();
		}
		switch(player) {
		case PlayerOne:
			player = Player.PlayerTwo;
			break;
		case PlayerTwo:
			player = Player.PlayerOne;
			break;
		}
	}

	public static void printGame() {
		System.out.println("P2 -> \t|6|\t|5|\t|4|\t|3|\t|2|\t|1|");
		System.out.print(" " + Board[0][6]);
		for (int j = 5; j >= 0; j--) {
			System.out.print("\t " + Board[0][j]);
		}
		System.out.print("\n  ");
		for (int j = 0; j <= 6; j++) {
			System.out.print("\t " + Board[1][j]);
		}
		System.out.println("\n\t|1|\t|2|\t|3|\t|4|\t|5|\t|6|\t <- P1");
		System.out.println("");
	}

	public static boolean updateGame(int Number) {
		boolean hasTurn = false;
		int playerSide = player.side;
		int indexValueOfNumber = Number - 1;
		int numberOfBalls = Board[playerSide][indexValueOfNumber];
		Board[playerSide][indexValueOfNumber] = 0;
		int i = indexValueOfNumber+1;
		while(numberOfBalls>0) {
			if(i == 6) {
				if(playerSide != player.side) {
					i = 0;
					playerSide = playerSide == 1 ? 0 : 1;
				}
				else {
					Board[playerSide][i] ++;
					numberOfBalls--;
					i = 0;
					playerSide = playerSide == 1 ? 0 : 1;
				}
			}
			else {
				Board[playerSide][i] ++;
				numberOfBalls--;
				i++;
			}
		}
		
		if(i == 0) {
			System.out.println("Extra turn");
			hasTurn = true;
		}
		else if(playerSide == player.side && Board[playerSide][i-1] == 1 && Board[playerSide == 1 ? 0 : 1][5-(i-1)] >0){
			System.out.println("Captured " + i);
			Board[playerSide][6] += Board[playerSide == 1 ? 0 : 1][5-(i-1)] + 1;
			Board[playerSide][i-1] = 0;
			Board[playerSide == 1 ? 0 : 1][5-(i-1)] = 0;
		}
		return hasTurn;
		
	}
	

	public static void checkGameState() {
		int side = player.side;
		int otherSide = side == 0 ? 1 : 0;
		boolean emptyBowls = true;
		boolean emptyOtherSideBowls = true;
		for (int i = 0; i < 6; i++) {
			if (Board[side][i] != 0)
				emptyBowls = false;
			if (Board[otherSide][i] != 0)
				emptyOtherSideBowls = false;
		}

		if (emptyBowls) {
			for (int i = 0; i < 6; i++) {
				Board[side][6] += Board[otherSide][i];
				Board[otherSide][i] = 0;
			}
			finished = true;
		}
		
		if (emptyOtherSideBowls) {
			for (int i = 0; i < 6; i++) {
				Board[otherSide][6] += Board[side][i];
				Board[side][i] = 0;
			}
			finished = true;
		}

	}
	
	public static void printScores() {
		System.out.println("Player 1 score: " + Board[1][6]);
		System.out.println("Player 2 score: " + Board[0][6]);
		System.out.println(Board[1][6] > Board[0][6] ? "Player 1 wins!!!" : "Player 2 wins!!!");
	}

	public static boolean isFinished() {
		return finished;
	}

}