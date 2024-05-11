

int contaPalindromo(char vetor[], int n){
  int numeroTotalPalindromos = 0; // Numero total de palindromos
  bool MatrizResposta[n][n];     // Matriz utilizada na programação dinâmica para resolução do problema
  memset(MatrizResposta,false,sizeof(MatrizResposta)) // Função para preencher toda a matriz com 'false'
  
  for(int i = 0; i < n; i++){
    MatrizResposta[i][i] = true; // Preenche a linha diagonal da matriz com 'true'
  }
  
  for(int tamanho = 2; tamanho <= n; tamanho++){ // 'tamanho' seria o tamanho do palíndromo
    for(int i = 0; i <= n-tamanho;i++){
      int j = tamanho + i - 1;
      if(i == j-1){ // aqui ele faz a análise para palíndromos de tamanho 2, o qual basta comparar a posição atual com o seu sucessor
        MatrizResposta[i][j] = (vetor[i] == vetor[j]);
      } else{
        MatrizResposta[i][j] = (vetor[i] == vetor[j] && MatrizResposta[i+1][j-1]);
      }
      if(MatrizResposta[i][j]){
        numeroTotalPalindromos++; 
      }
    }
  }
  return numeroTotalPalindromos;
}
