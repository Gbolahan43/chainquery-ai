import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { chainQueryApi } from '@/lib/api';
import { getSessionId } from '@/lib/auth';

export interface QueryResponse {
  id: string;
  user_input: string;
  sql_output: string;
  created_at: string;
  error_message: string | null;
  chain: string;
}

interface GenerateRequest {
  user_input: string;
  chain: string;
}

export function useHistory() {
  const sessionId = getSessionId();

  return useQuery({
    queryKey: ['history', sessionId],
    queryFn: async () => {
      return await chainQueryApi.getHistory(sessionId);
    },
    enabled: !!sessionId,
  });
}

export function useGenerateSQL() {
  const queryClient = useQueryClient();
  const sessionId = getSessionId();

  return useMutation({
    mutationFn: async (data: GenerateRequest) => {
      return await chainQueryApi.generate(data.user_input, data.chain, sessionId);
    },
    onSuccess: () => {
      // Refetch history when a new query is generated
      queryClient.invalidateQueries({ queryKey: ['history'] });
    },
  });
}

