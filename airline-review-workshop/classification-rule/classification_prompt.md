# Classification task

Classify each airline customer review using the supplied topic taxonomy.

Identify every service aspect covered by the taxonomy that receives a clear evaluation. Assign one sentiment to each selected aspect.

## Rules

- Use only topics and sentiment labels from the taxonomy.
- Do not classify an aspect that is merely mentioned.
- Classify the target of the evaluation, not the words used as evidence. A mention of food, prices, or seats does not by itself select those topics — ask what the reviewer is actually evaluating.
- Return each topic at most once. If a topic receives both positive and negative evaluation, assign it the sentiment `mixed`.
- Use `food_and_beverages` for catering experienced in service: onboard meals, drinks, menu choice, and availability. Food and drinks in airport lounges are part of the lounge experience and belong to `airport_and_ground_service`.
- Failures of pre-departure processes — misinformation before travel, lost requests such as special meals, seat assignment errors — belong to `booking_and_preflight`, even when they involve food or seats.
- Use `flight_operations` for whether flights ran as planned — punctuality, delays, cancellations, connections, rebooking — and the airline's assistance during such disruptions. Evaluations of airport facilities and ground staff service belong to `airport_and_ground_service`.
- Services outside the flight and airport experience (for example chauffeur transfers and loyalty programmes) are out of scope. Do not classify them, and do not place them under `other_or_unclear`.
- Use `overall_experience` only when the review gives a clear general evaluation but does not evaluate any specific service aspect.
- Use `other_or_unclear` only when the review evaluates no taxonomy-covered aspect and `overall_experience` does not apply.
- Always return at least one aspect. If no specific service aspect is evaluated, fall back to `overall_experience`, and then to `other_or_unclear`.
- Set `review_required` to `true` when the classification is substantially ambiguous. Still provide the best available classification. When `review_required` is true, include a `review_reason` field briefly explaining the ambiguity.
- Return valid JSON that matches the supplied output schema.
