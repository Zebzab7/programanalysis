package student.dtu;

import java.util.ArrayList;
import java.util.List;

import student.dtu.AI.Node;
import student.dtu.Game.Player;

public class AI {
	
	//This controls the depth that miniMax searches
	private int maxRecursionDepth = 5;
	private static Player player;
	private static Player otherPlayer;
	
	public AI(Player player) {
		AI.player = player;
		AI.otherPlayer = AI.player == Player.PlayerTwo ? Player.PlayerOne 
				: Player.PlayerTwo;
	}
	
	public static class Node {
		private int depth;
		private short[][] gameState = new short[2][7];
		private Node parent;
		private boolean isTerminated;
		private boolean isMax;
		private short move;
		private List<Node> neighbors;
		
		public Node(short[][] gameState, boolean isMax, int depth,
				boolean isTerminated, Node parent, short move) {
			for(int i = 0; i < gameState.length; i++) {
				for(int j = 0; j < gameState[i].length; j++) {
					this.gameState[i][j] = gameState[i][j];
				}
			}
			this.isMax = isMax;
			this.depth = depth;
			this.isTerminated = isTerminated;
			this.parent = parent;
			this.move = move;
			this.neighbors = new ArrayList<Node>();
		}

		public boolean isTerminated() {
			return isTerminated;
		}
		
		//Getters and setters
		public short[][] getGameState() {
			return gameState;
		}

		public List<Node> getNeighbors() {
			return neighbors;
		}
		
		public void addNeighbor(Node node) {
			neighbors.add(node);
		}
		public short getMove() {
			return move;
		}
		public boolean isMax() {
			return isMax;
		}

		public int getDepth() {
			return depth;
		}

		public void setDepth(int depth) {
			this.depth = depth;
		}

		public Node getParent() {
			return parent;
		}

		public void setParent(Node parent) {
			this.parent = parent;
		}
	}
	
	public Node simulateGame(Node node, short move) {
		
		if(isValidMove(node, move)) {
			return aiTurnSimulate(node, move);
		}
		
		return null;
	}
	
	/*
	 * SECTION 1: AI Logic
	 */
	
	//Generates neighbors for the miniMax tree
	public void generateNeighbors(Node node) {
		Node neighborNode = null;
		for(short i = 1; i <= 6; i++) {
			neighborNode = simulateGame(node, i);
			
			if(neighborNode != null) {
				node.addNeighbor(neighborNode);
			}	
		}
	}
	
	public int miniMax(Node node) {
		
		//Terminal-test
		if(node.isTerminated() || node.depth == maxRecursionDepth) {
			return player == Player.PlayerOne ? evalBase(node.getGameState()) : evalBase(node.getGameState());
		}
		
		if(node.isMax()) {
			int max = Integer.MIN_VALUE;
			generateNeighbors(node);
			for (Node neighbor : node.getNeighbors()) {
				max = Math.max(max, miniMax(neighbor));
			}
			return (short) max;			
		}
		
		//Player is min
		if(!node.isMax()) {
			int min = Integer.MAX_VALUE;
			generateNeighbors(node);
			for (Node neighbor : node.getNeighbors()) {
				min = Math.min(min, miniMax(neighbor));
			}
			return (short) min;
		}
		
		//Error
		System.out.println("miniMax failed");
		return -1;
		
	}
	
	//Base evaluation function
	public int evalBase(short[][] state) {
		short opponentPoints = state[otherPlayer.side][6];
		short aiPoints = state[player.side][6];
		return aiPoints - opponentPoints;
	}
	
	//Evaluation function 2
	public int evalEmptySpaces(short[][] state) {
        short opponentEmptySpaces = 0;
        short aiEmptySpaces = 0;
        for(int i = 0; i < 6; i++) {
            if(state[otherPlayer.side][i] == 0) {
                opponentEmptySpaces++;
            }
            if(state[player.side][i] == 0) {
                aiEmptySpaces++;
            }
        }
        return (opponentEmptySpaces - aiEmptySpaces) + evalBase(state);
	}
	
	//This method chooses the best move for the AI to take based on the miniMax
	//Algorithm
	public int aiMove(Node source) {
		generateNeighbors(source);
		int minValue = Integer.MIN_VALUE;
		short bestMove = -1;
		for(Node neighbor : source.getNeighbors()) {
			int miniMaxRes = miniMax(neighbor);
			if(miniMaxRes > minValue) {
				minValue = miniMaxRes;
				bestMove = neighbor.getMove();
			}
		}
		System.out.println("Evaluation: " + minValue);
		return bestMove;
	}
	
	/*
	 * SECTION 2: Game logic
	 */
	public boolean isValidMove(Node node, short move) {
		short[][] gameState = node.getGameState();
		boolean isMax = node.isMax();
		
		if(gameState[isMax?player.side:otherPlayer.side][move-1] != 0) {
			return true;
		}
		
		return false;	
	}
	
	public static Node aiTurnSimulate(Node node,short move){
		short[][] newGameState = new short[2][7];
		short[][] parentGameState = node.getGameState();
		for(int i = 0; i < parentGameState.length; i++) {
			for(int j = 0; j < parentGameState[i].length; j++) {
				newGameState[i][j] = parentGameState[i][j];
			}
		}
		Player aiPlayer = node.isMax() ? player : otherPlayer;
		boolean hasNextTurn = updateAiGame(newGameState,aiPlayer,move);
		if(aiPlayer == otherPlayer) {
			hasNextTurn = !hasNextTurn;
		}
		boolean finished = checkAiGameState(newGameState, aiPlayer);
		return new Node(newGameState, hasNextTurn, node.getDepth() + 1, finished, node, move);
	}
	
	public static boolean updateAiGame(short[][] gameState,Player aiPlayer,short move) {
		boolean hasTurn = false;
		int playerSide = aiPlayer.side;
		int indexValueOfNumber = move - 1;
		int numberOfBalls = gameState[playerSide][indexValueOfNumber];
		gameState[playerSide][indexValueOfNumber] = 0;
		int i = indexValueOfNumber+1;
		while(numberOfBalls>0) {
			if(i == 6) {
				if(playerSide != aiPlayer.side) {
					i = 0;
					playerSide = playerSide == 1 ? 0 : 1;
				}
				else {
					gameState[playerSide][i] ++;
					numberOfBalls--;
					i = 0;
					playerSide = playerSide == 1 ? 0 : 1;
				}
			}
			else {
				gameState[playerSide][i] ++;
				numberOfBalls--;
				i++;
			}
		}
		
		if(i == 0) {
			hasTurn = true;
		}
		else if(playerSide == aiPlayer.side && gameState[playerSide][i-1] == 1 && gameState[playerSide == 1 ? 0 : 1][5-(i-1)] >0){
			gameState[playerSide][6] += gameState[playerSide == 1 ? 0 : 1][5-(i-1)] + 1;
			gameState[playerSide][i-1] = 0;
			gameState[playerSide == 1 ? 0 : 1][5-(i-1)] = 0;
		}
		return hasTurn;
		
	}
	
	public static boolean checkAiGameState(short[][]gameState,Player aiPlayer) {
//		boolean aiFinished = false;
//		int side = aiPlayer.side;
//		int otherSide = side == 0 ? 1 : 0;
//		boolean emptyBowls = true;
//		for (int i = 0; i < 6; i++) {
//			if (gameState[side][i] != 0)
//				emptyBowls = false;
//		}
//		if (emptyBowls) {
//			for (int i = 0; i < 6; i++) {
//				gameState[side][6] += gameState[otherSide][i];
//				gameState[otherSide][i] = 0;
//			}
//			aiFinished = true;
//		}
//		return aiFinished;
		
		boolean aiFinished = false;
		int side = aiPlayer.side;
		int otherSide = side == 0 ? 1 : 0;
		boolean emptyBowls = true;
		boolean emptyOtherSideBowls = true;
		for (int i = 0; i < 6; i++) {
			if (gameState[side][i] != 0)
				emptyBowls = false;
			if (gameState[otherSide][i] != 0)
				emptyOtherSideBowls = false;
		}

		if (emptyBowls) {
			for (int i = 0; i < 6; i++) {
				gameState[side][6] += gameState[otherSide][i];
				gameState[otherSide][i] = 0;
			}
			aiFinished = true;
		}
		
		if (emptyOtherSideBowls) {
			for (int i = 0; i < 6; i++) {
				gameState[otherSide][6] += gameState[side][i];
				gameState[side][i] = 0;
			}
			aiFinished = true;
		}
		return aiFinished;
		
	}
//
//	public int getMaxRecursionDepth() {
//		return maxRecursionDepth;
//	}
//
//	public void setMaxRecursionDepth(int maxRecursionDepth) {
//		this.maxRecursionDepth = maxRecursionDepth;
//	}
//	
	
}
